from django.shortcuts import render, HttpResponse
from .models import Email

# Create your views here.
def home(request):
    return render(request, "home.html")

def emails(request):
    items = Email.objects.all()
    return render(request, "emails.html", {"emails": items})

