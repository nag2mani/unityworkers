import requests
import random

def send_otp(mobile_number):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP

    # Define your MSG91 API credentials
    api_key = '431888AxYqD1oBfcB671129e4P1'
    sender_id = 'your_sender_id'
    message = f"Your OTP is {otp}"

    # Send OTP via MSG91
    url = f"https://api.msg91.com/api/sendhttp.php"
    payload = {
        'authkey': api_key,
        'mobiles': mobile_number,
        'message': message,
        'sender': sender_id,
        'route': '4',  # Use '4' for promotional messages; '1' for transactional messages
        'country': '91'  # India
    }

    response = requests.post(url, data=payload)

    # Store the OTP in session (optional)
    # You may want to store it in a more secure manner in a production app
    return otp
