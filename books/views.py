from django.shortcuts import render
from django.views.generic import CreateView, DetailView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404,redirect
from django.urls import reverse_lazy
from . import models
from .forms import BookForm,ReviewForm,BookDonationForm
from . import forms
from author.models import UserAccount
from .models import BuyBook,Category,Book,Review
from django. contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_list_or_404 
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import DonatedBook

def send_transaction_email(user, subject, template):
    message = render_to_string(template, {
        'user': user,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

def book_view(request,category_slug=None):
    categories=Category.objects.all()

    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        data=Book.objects.filter(category=category)

    else:
        data=Book.objects.all()

    return render(request,'book_list.html',{'data':data,'categories':categories})


@method_decorator(login_required, name='dispatch')
class DetailsPost(DetailView):
    model = models.Book
    pk_url_kwarg = 'pk'
    template_name = 'book_details.html'

        
    def post(self, request, *args, **kwargs):
        comment_form = forms.ReviewForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments.all()
        comment_form = forms.ReviewForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
    

@login_required
def buy_book(request,book_id):
    book=get_object_or_404(Book,pk=book_id)
    if request.method=='GET':
        return render(request,'buy_book.html',{'book':book})

    elif request.method=='POST':
        if request.user.account.balance>=book.buying_price:
            request.user.account.balance-=book.buying_price
            request.user.account.save()
            BuyBook.objects.create(user=request.user,book=book)
            messages.success(request, f"You have successfully bought {book.title}.")
        else:
            messages.error(request, "Insufficient funds to buy the book.")

        send_transaction_email(request.user, "Bought Message", "buy_email.html")
        return redirect('book_list')


class MyBookListView(ListView):
    template_name = 'mybook_list.html'
    context_object_name = 'data'   

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            user_books = BuyBook.objects.filter(user=self.request.user, book__category=category).select_related('book')
        else:
            user_books = BuyBook.objects.filter(user=self.request.user).select_related('book')

        return [user_book.book for user_book in user_books]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['user_books'] = BuyBook.objects.filter(user=self.request.user).select_related('book')
        context['user_donated_books'] = DonatedBook.objects.filter(user=self.request.user).select_related('book')
        return context


def donate_book(request, book_id):
    user_books = get_list_or_404(BuyBook, user=request.user, book__pk=book_id)
    if user_books:
        donated_book = DonatedBook(user=request.user, book=user_books[0].book)
        donated_book.save()
        donation_date = donated_book.donation_date
        request.user.account.coin_balance += 1
        request.user.account.save()
        user_books[0].delete()
        messages.success(request, f"You have successfully donated {donated_book.book.title}.")
        return redirect('my_book')
    
    messages.error(request, "No book found to donate.")
    return redirect('my_book')