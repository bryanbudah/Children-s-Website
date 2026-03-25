from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .mpesa import MpesaService
from django.views.decorators.csrf import csrf_exempt
import json


# Home view
def home(request):
    return JsonResponse({
        "message": "Welcome to the Children's Home donation site!"
    })


# Donation view
@csrf_exempt
def donate(request):
    if request.method == "POST":
        try:
            # Handle JSON requests (e.g., from frontend or Postman)
            if request.content_type == "application/json":
                data = json.loads(request.body)
                phone = data.get("phone")
                amount = data.get("amount")
            else:
                # Handle form submissions (HTML form)
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
        # 👉 Show HTML donation page instead of JSON
        return render(request, "donate.html")

    return HttpResponseBadRequest("Invalid request method")


# M-Pesa callback view
@csrf_exempt
def mpesa_callback(request):
    """
    Receives M-Pesa payment responses (STK Push)
    """
    if request.method == "POST":
        try:
            payload = json.loads(request.body)

            print("========== M-PESA CALLBACK ==========")
            print(json.dumps(payload, indent=2))
            print("=====================================")

            # OPTIONAL: Extract useful data
            body = payload.get("Body", {})
            stk_callback = body.get("stkCallback", {})

            result_code = stk_callback.get("ResultCode")
            result_desc = stk_callback.get("ResultDesc")

            print("Result Code:", result_code)
            print("Result Desc:", result_desc)

            # TODO: Save transaction to database

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