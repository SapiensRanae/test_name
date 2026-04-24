from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render

from apps.core.models import Creator


# Create your views here.

def about_view(request):
    return HttpResponse("About page")

def welcome_view(request):
    return render(request, 'core/welcome.html')


def creator_view(request):
    if request.method == "POST":
        data = {
            "email": request.POST.get("email"),
        }
    try:
        creator = Creator(**data)
        creator.full_clean()
        creator.save()
    except ValidationError as e:
        error_message = e.message_dict
    return render(request, 'core/creator.html')