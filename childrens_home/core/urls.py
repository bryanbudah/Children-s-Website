# core/urls.py
from django.urls import path
from .views import mpesa_callback, donate
from . import views
from .views import upload_image

urlpatterns = [
   path("", views.home, name="home"),
    path("gallery/", views.gallery, name="gallery"),
    path("mpesa-donate/", views.donate, name="donate"), 
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),

 # Placeholder for future Donate Online page, 
   path("donate/", views.donate_online, name="donate_online"),# temporary placeholder
    path("create-checkout-session/", views.create_checkout_session),
        # ✅ ADD THIS (IMPORTANT)
    path("simulate-payment/", views.simulate_payment, name="simulate_payment"),

  path("upload/", upload_image, name="upload"),
]