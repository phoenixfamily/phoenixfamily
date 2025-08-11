from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp_code):
    """
    Sends an OTP code to the given email.
    """
    subject = "Your OTP Code"
    message = f"Your OTP: {otp_code}. This code is valid for 5 minutes."
    from_email = settings.DEFAULT_FROM_EMAIL  # Use email defined in settings.py
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
