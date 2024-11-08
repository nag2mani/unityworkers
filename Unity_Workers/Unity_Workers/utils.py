# otp_verification/utils.py
from twilio.rest import Client
from django.conf import settings
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(phone_number, otp_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = f"Your OTP code is {otp_code}"
    client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
