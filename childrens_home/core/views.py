from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
import random

from .mpesa import MpesaService
from .models import TestImage


# =========================
# STRIPE KEY
# =========================
stripe.api_key = "YOUR_SECRET_KEY"


# =========================
# PAGES
# =========================

def home(request):
    return render(request, "core/home.html")


def gallery(request):
    return render(request, "core/gallery.html")


def donate_online(request):
    return render(request, "core/donate_online.html")


# =========================
# M-PESA DONATION
# =========================

@csrf_exempt
def donate(request):
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)
                phone = data.get("phone")
                amount = data.get("amount")
            else:
                phone = request.POST.get("phone")
                amount = request.POST.get("amount")

            if not phone or not amount:
                return JsonResponse({"error": "Phone and amount are required"}, status=400)

            response = MpesaService.stk_push(phone, amount)

            return JsonResponse({
                "status": "Request sent",
                "mpesa_response": response
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "GET":
        return render(request, "donate.html")

    return HttpResponseBadRequest("Invalid request method")


# =========================
# STRIPE PAYMENT
# =========================

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = int(data.get("amount")) * 100

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "Donation"},
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url="http://127.0.0.1:8000/",
                cancel_url="http://127.0.0.1:8000/",
            )

            return JsonResponse({"id": session.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# =========================
# M-PESA CALLBACK
# =========================

@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)

            print("========== M-PESA CALLBACK ==========")
            print(json.dumps(payload, indent=2))
            print("=====================================")

            stk_callback = payload.get("Body", {}).get("stkCallback", {})

            print("Result Code:", stk_callback.get("ResultCode"))
            print("Result Desc:", stk_callback.get("ResultDesc"))

            return JsonResponse({
                "ResultCode": 0,
                "ResultDesc": "Callback received successfully"
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "ResultCode": 1,
                "ResultDesc": "Invalid JSON"
            }, status=400)

    return JsonResponse({
        "ResultCode": 1,
        "ResultDesc": "Method not allowed"
    }, status=405)


# =========================
# TEST PAYMENT
# =========================

def simulate_payment(request):
    if request.method == "POST":
        return JsonResponse({
            "transaction_id": f"SIM{random.randint(100000,999999)}"
        })

    return JsonResponse({"error": "Only POST allowed"}, status=405)


# =========================
# IMAGE UPLOAD (CLOUDINARY TEST)
# =========================

def upload_image(request):
    print("STORAGE:", default_storage)

    if request.method == "POST":
        print("POST DATA:", request.POST)
        print("FILES:", request.FILES)

        name = request.POST.get("name")
        image = request.FILES.get("image")

        if not name or not image:
            return JsonResponse({
                "error": "Missing name or image",
                "debug_post": dict(request.POST),
                "debug_files": str(request.FILES)
            }, status=400)

        obj = TestImage.objects.create(name=name, image=image)

        return render(request, "upload.html", {
            "image_url": obj.image.url
        })

    return render(request, "upload.html")