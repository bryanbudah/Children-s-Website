# core/urls.py
from django.urls import path
from .views import mpesa_callback, donate
from . import views

urlpatterns = [
   path("", views.home, name="home"),
    path("gallery/", views.gallery, name="gallery"),
    path("mpesa-donate/", views.donate, name="donate"), 
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),

 # Placeholder for future Donate Online page
    path("donate-online/", views.home, name="donate_online"),  # temporary placeholder

]