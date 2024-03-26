from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("emails/", views.emails, name="emails"),
    ]
