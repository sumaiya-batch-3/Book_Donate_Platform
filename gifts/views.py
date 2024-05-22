from django.shortcuts import render
from django.views.generic import CreateView, DetailView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404,redirect
from django.urls import reverse_lazy
from . import models
from . import forms
from author.models import UserAccount
from .models import RedeemBook,GiftBook
from django. contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_list_or_404 
from django.views import View


@login_required
def redeem_book(request, book_id):
    book = get_object_or_404(GiftBook, pk=book_id)
    if request.method == 'GET':
        return render(request, 'buy_book.html', {'book': book})
    elif request.method == 'POST':
        if request.user.account.coin_balance >= book.buying_price:
            request.user.account.coin_balance -= book.buying_price
            request.user.account.save()
            RedeemBook.objects.create(user=request.user, book=book)
            messages.success(request, f"You have successfully redeemed {book.title}.")
        else:
            messages.error(request, "Insufficient funds to redeem the book.")
        return redirect('book_wise_post')

@login_required
def book_view(request):
    data = GiftBook.objects.all()
    redeemed_books = RedeemBook.objects.filter(user=request.user)
    return render(request, 'book_list_gifts.html', {'data': data, 'redeemed_books': redeemed_books})
