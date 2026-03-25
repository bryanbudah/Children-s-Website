import requests
import base64
from datetime import datetime

def lipa_na_mpesa(phone, amount):

    shortcode = "174379"
    passkey = "YOUR_PASSKEY"

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    password = base64.b64encode(
        (shortcode + passkey + timestamp).encode()
    ).decode()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://yourdomain.com/mpesa/callback/",
        "AccountReference": "Donation",
        "TransactionDesc": "Donation Payment"
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    response = requests.post(url, json=payload)

    return response.json()