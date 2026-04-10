from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def about_view(request):
    return HttpResponse("About page")

def welcome_view(request):
    return render(request, 'core/welcome.html')