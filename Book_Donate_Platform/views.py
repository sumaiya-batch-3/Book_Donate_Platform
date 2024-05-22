from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

def about_view(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')