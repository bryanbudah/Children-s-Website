from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .mpesa import MpesaService
import json
import stripe


# 🔑 Stripe Secret Key (replace with your real key later)
stripe.api_key = "YOUR_SECRET_KEY"


# =========================
# HOME & PAGES
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
            # Handle JSON requests
            if request.content_type == "application/json":
                data = json.loads(request.body)
                phone = data.get("phone")
                amount = data.get("amount")
            else:
                # Handle form submissions
                phone = request.POST.get("phone")
                amount = request.POST.get("amount")

            # Validation
            if not phone or not amount:
                return JsonResponse({
                    "error": "Phone and amount are required"
                }, status=400)

            # Call M-Pesa service
            response = MpesaService.stk_push(phone, amount)

            return JsonResponse({
                "status": "Request sent",
                "mpesa_response": response
            })

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)

    elif request.method == "GET":
        return render(request, "donate.html")

    return HttpResponseBadRequest("Invalid request method")


# =========================
# STRIPE CARD PAYMENT
# =========================

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = int(data.get("amount")) * 100  # convert to cents

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Donation",
                        },
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

            body = payload.get("Body", {})
            stk_callback = body.get("stkCallback", {})

            result_code = stk_callback.get("ResultCode")
            result_desc = stk_callback.get("ResultDesc")

            print("Result Code:", result_code)
            print("Result Desc:", result_desc)

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