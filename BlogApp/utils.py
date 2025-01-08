import pyotp
from datetime import datetime,timedelta
from django.conf import settings
from django.core.mail import send_mail
import random

def send_otp(request,email):       #used in login
    totp=pyotp.TOTP(pyotp.random_base32(),interval=120)
    otp=totp.now()
    request.session['otp_secret_key']=totp.secret
    valid_date=datetime.now() + timedelta(minutes=3)
    request.session['otp_valid_data']=str(valid_date)

    print(f'your otp  is {otp} : ')

    send_mail(
                "Password Notification",
                f'your otp  is {otp} : ',
                settings.EMAIL_HOST_USER,
                # ['kash123@yopmail.com'],
                [email],
                fail_silently=False,
            )


def send_email_token(email,token):
    print('this is email',email)

    print(f'click on the link to verify http://127.0.0.1:8000/verify_email/{token}')

    send_mail(
                "Password Notification",
                f'click on the link to verify http://127.0.0.1:8000/verify/{token} ',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
    # return True



def generate_otp():
    
    return random.randint(100000, 999999)

# This function sends the OTP to the user's email
def send_verification_email(email, otp):

    print('password reset otp : ',otp)

    subject = 'Your OTP for Password Reset'
    message = f'Your OTP for resetting your password is: {otp}'
    send_mail(subject, message, 'kalashs051101@gmail.com.com', [email])  # Update 'from@example.com' with your email

