from django.shortcuts import redirect
from django.contrib import messages


# Custom view decorators to prevent manual page navigation

def login_required(function):   
    def wrap(request, *args, **kwargs):
        if "user_id" in request.session:
            return function(request, *args, **kwargs)

        else:
            messages.info(request, "Log into your account first")
            return redirect("login")

    return wrap  


def not_logged_in(function):
    def wrap(request, *args, **kwargs):
        if "user_id" in request.session:
            messages.info(request, "Log out from your account to continue")
            return redirect("portfolio")

        else:
            return function(request, *args, **kwargs)

    return wrap 


def mail_required(function):
    def wrap(request, *args, **kwargs):
        if "mail" in request.session:
            return function(request, *args, **kwargs)

        else:
            messages.info(request, "Enter your email to continue")
            return redirect("register")

    return wrap   


def otp_required(function):
    def wrap(request, *args, **kwargs):
        if "otp" in request.session:
            return function(request, *args, **kwargs)

        else:
            messages.info(request, "Please enter your email first")
            return redirect("register")

    return wrap  


def mail_validation_required(function):
    def wrap(request, *args, **kwargs):
        if "verified" in request.session:
            return function(request, *args, **kwargs)

        else:
            messages.info(request, "Please verify your email first")
            return redirect("validate_mail")

    return wrap 


def details_required(function):    
    def wrap(request, *args, **kwargs):
        if "username" in request.session:
            return function(request, *args, **kwargs)

        else:
            messages.info(request, "Enter your details to continue")
            return redirect("open_account")

    return wrap 


def pass_required(function):    
    def wrap(request, *args, **kwargs):
        if "password" in request.session:
            return function(request, *args, **kwargs)

        else:
            messages.info(request, "Create a password for your account")
            return redirect("create_pass")

    return wrap 

    
def user_validation_required(function):
    def wrap(request, *args, **kwargs):
        if "user" in request.session:
            return function(request, *args, **kwargs)

        else:
            messages.info(request, "Please confirm your email first")
            return redirect("confirm_mail")

    return wrap 

   