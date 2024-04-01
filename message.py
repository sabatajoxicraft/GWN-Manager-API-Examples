import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_SMS_number = os.getenv("TWILIO_PHONE_NUMBER")
from_WA_number = os.getenv("TWILIO_WHATSAPP_NO")

client = Client(account_sid, auth_token)

def send_sms_message(to_number, voucher_password):
    body_message = f'Hi Sebanebane Wa Kae-Kae, Your WIFI voucher password is:  + {voucher_password}'

    message = client.messages.create(
                    body = body_message,
                    from_ = from_SMS_number,
                    to = to_number
                )

    return message.sid

def send_WA_message(to_number, voucher_password):
    body_message = f'Hi Sebanebane Wa Kae-Kae, Your WIFI voucher password is:  + {voucher_password}'

    message = client.messages.create(
        from_=from_WA_number,
        body=body_message,
        to=f'whatsapp:{to_number}'
    )

    print(message.sid)