import requests
import base64
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class MpesaService:
    """
    Handles all M-Pesa API interactions with debug info
    """

    def __init__(self, environment="sandbox"):
        """
        environment: "sandbox" or "production"
        """
        self.environment = environment.lower()
        self.base_url = (
            "https://sandbox.safaricom.co.ke" if self.environment == "sandbox"
            else "https://api.safaricom.co.ke"
        )

    @staticmethod
    def format_phone_number(number):
        """
        Converts Kenyan numbers to international format (2547XXXXXXXX)
        """
        clean = number.replace(" ", "").replace("-", "").replace("+", "")
        if clean.startswith("0"):
            clean = "254" + clean[1:]
        return clean

    def get_access_token(self):
        """
        Generate M-Pesa access token with debug info
        """
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")

        print("Debug: Consumer Key:", consumer_key)
        print("Debug: Consumer Secret:", consumer_secret)

        if not consumer_key or not consumer_secret:
            raise Exception("Missing CONSUMER_KEY or CONSUMER_SECRET in environment variables.")

        response = requests.get(url, auth=(consumer_key, consumer_secret))
        if response.status_code != 200:
            print("Debug: Access token request failed:", response.text)
            raise Exception(f"Access token request failed with status {response.status_code}")

        data = response.json()
        access_token = data.get("access_token")
        if not access_token:
            raise Exception(f"Failed to get access token: {data}")
        print("Debug: Access token received")
        return access_token

    def stk_push(self, phone_number, amount):
        """
        Initiates STK Push with debug info and error handling
        """
        phone_number = self.format_phone_number(phone_number)
        print("Debug: Formatted phone number:", phone_number)

        access_token = self.get_access_token()

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        short_code = os.getenv("SHORTCODE")
        passkey = os.getenv("PASSKEY")
        callback_url = os.getenv("MPESA_CALLBACK_URL")

        print("Debug: Shortcode:", short_code)
        print("Debug: Passkey:", passkey)
        print("Debug: Callback URL:", callback_url)

        if not all([short_code, passkey, callback_url]):
            raise Exception("SHORTCODE, PASSKEY, or MPESA_CALLBACK_URL missing from environment variables.")

        password = base64.b64encode((short_code + passkey + timestamp).encode()).decode('utf-8')

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": "TestDonation",
            "TransactionDesc": "Children Home Donation Sandbox"
        }

        print("Debug: STK Push payload:", payload)

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()  # raise HTTPError for 4xx/5xx
            data = response.json()
            print("Debug: STK Push response:", data)
            return data
        except requests.exceptions.RequestException as e:
            print("STK Push failed:", e)
            return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    mpesa = MpesaService(environment="sandbox")
    # Use sandbox test number
    response = mpesa.stk_push(phone_number="254700000001", amount=100)
    print(response)