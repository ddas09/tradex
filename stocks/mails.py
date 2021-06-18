import math, random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# Provides different services for sending automated emails

# Generates a random 6 digit OTP for email verification
def generateOTP():
    digits = "0123456789"
    OTP = ""

    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP    


def sendOTP(user_email):
    # Generate an OTP for the user
    generated_otp = generateOTP()

    # Html content of email
    html_message = render_to_string("mails/mail_validation.html", {"otp": generated_otp})

    # Create a object to send the email
    email = EmailMessage(
        subject = "Verify your email", 
        body = html_message,
        from_email = "TradeX Email Verification <" + settings.EMAIL_HOST_USER + ">", 
        to = [user_email],
    )

    # this is required because there is no plain text email message
    email.content_subtype = "html" 

    email.send(fail_silently = True)
    return generated_otp


def sendMailVerified(user_email):
    # Html content of email
    html_message = render_to_string("mails/mail_verified.html", {"mail": user_email})

    # Create a object to send the email
    email = EmailMessage(
        subject = "Email verification successfull", 
        body = html_message,
        from_email = "TradeX Customer Support <" + settings.EMAIL_HOST_USER + ">", 
        to = [user_email],
    )

    email.content_subtype = "html" 
    email.send(fail_silently = True)


def getPlanPrice(plan_type):
    if plan_type == "S":
        return 10
    elif plan_type == "P":
        return 25
    elif plan_type == "E":
        return 50


def sendAccountCreated(request, date):
    # Data to be passed to mail template
    user_name = request.session["first_name"] + " " + request.session["last_name"]
    card_number = request.session["card_number"]
    user_email = request.session["mail"]
    plan = request.session["plan_type"]
    price = getPlanPrice(plan[0])

    html_message = render_to_string(
        "mails/account_created.html", 
        {"user": user_name, "plan": plan, "card": card_number, "price": price, "timestamp": date}
    )

    email = EmailMessage(
        subject = "Welcome to TradeX!", 
        body = html_message,
        from_email = "TradeX Inc <" + settings.EMAIL_HOST_USER + ">", 
        to = [user_email],
    )

    email.content_subtype = "html" 
    email.send(fail_silently = True)

  
