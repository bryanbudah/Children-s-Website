# core/urls.py
from django.urls import path
from .views import mpesa_callback, donate

urlpatterns = [
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),

path("donate/", donate, name="donate"),
]