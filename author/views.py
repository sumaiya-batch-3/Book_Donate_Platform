from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout,authenticate
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
from django.http import HttpResponse
# from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

class UserRegistrationView(FormView):
    template_name='user_registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('profile')

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user=form.save()
            # token=default_token_generator.make_token(user)
            # uid=urlsafe_base64_encode(force_bytes(user.pk))
            # confirm_link=f"http://127.0.0.1:8000/author/active/{uid}/{token}"
            # email_subject="Confirm Your Email"
            # email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link})
            # email=EmailMultiAlternatives(email_subject,'',to=[user.email])
            # email.attach_alternative(email_body,"text/html")
            # email.send()
            return HttpResponse("Registration successful")
        
        
        return self.form_invalid(form)


# class UserRegistrationView(FormView):
#     template_name = 'user_registration.html'
#     form_class = UserRegistrationForm
#     success_url = reverse_lazy('profile')

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         confirm_link = f"http://127.0.0.1:8000/author/active/{uid}/{token}"
#         email_subject = "Confirm Your Email"
#         email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
#         email = EmailMultiAlternatives(email_subject, '', to=[user.email])
#         email.attach_alternative(email_body, "text/html")
#         email.send()

#         return HttpResponse("Check your email for confirmation")

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(data=request.POST)

#         if form.is_valid():
#             return self.form_valid(form)

#         return self.form_invalid(form)


# def activate(request, uid64, token):
#     try:
#         uid = urlsafe_base64_decode(uid64).decode()
#         user = User._default_manager.get(pk=uid)

#     except User.DoesNotExist:
#         user = None 

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return redirect('login')
#     else:
#         return redirect("register")        


class UserLoginView(LoginView):
    template_name = 'user_login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
    

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    

class UserAccountUpdateView(View):
    template_name='profile.html'

    def get(self,request):
        if request.user.is_authenticated:
            form=UserUpdateForm(instance=request.user)
            return render(request,self.template_name,{'form':form})
        else:
            return redirect('login')

    def post(self,request):
        if request.user.is_authenticated:
            form=UserUpdateForm(request.POST,instance=request.user)  
            if form.is_valid():
                form.save()
                messages.success(self.request,"User Profile Information Updated Successfully")
                return redirect('profile')
            return render(request,self.template_name,{'form':form})
        else:
            return redirect('login')
          