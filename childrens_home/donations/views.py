from django.shortcuts import render

# Create your views here.
import json
import time
from django.http import JsonResponse
from .models import Donation

def simulate_payment(request):
    data = json.loads(request.body)

    phone = data.get("phone")
    amount = data.get("amount")
    method = data.get("method")  # mpesa or card

    # Simulate delay (like real payment)
    time.sleep(2)

    donation = Donation.objects.create(
        amount=amount,
        phone=phone,
        payment_method=method,
        status="completed"
    )

    return JsonResponse({
        "status": "success",
        "message": "Payment successful",
        "transaction_id": f"TXN{donation.id:05d}"
    })