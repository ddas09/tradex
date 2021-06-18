from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

# Provides different functions for validating form data 

def validateEmail(email):
    # Validate user's email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False    


def validateName(name):
    valid_pattern = "[A-Za-z]{3,}"

    if re.match(valid_pattern, name):
        return True
    else:
        return False


def validateUsername(username):
    valid_pattern = "^[A-Za-z]{1}[A-Za-z0-9]{5,}$"

    if re.match(valid_pattern, username):
        return True
    else:
        return False


def validatePassword(password):
    valid_pattern = "(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-+/]).{8,}"

    if re.match(valid_pattern, password):
        return True
    else:
        return False    


def validateCardPattern(card_number):
    valid_pattern = "^(3[47][0-9]{13}|5[1-5][0-9]{14}|4[0-9]{12}(?:[0-9]{3})?)$"

    if re.match(valid_pattern, card_number):
        return True
    else:
        return False    


def validateCardType(card_type):
    allowed_card_types = ["AMEX", "VISA", "MASTERCARD"]

    if card_type in allowed_card_types:
        return True
    else:
        return False    


def validatePlanType(plan_type):
    allowed_plan_types = ["STARTER", "PROFESSIONAL", "ENTERPRISE"]

    if plan_type in allowed_plan_types:
        return True
    else:
        return False   


# Visit @https://cs50.harvard.edu/x/2021/psets/1/credit/ for details
def cardType(card_number):
    card_len = len(card_number)

    if card_len == 15 and re.match("^3[4-7]", card_number):
        return "AMEX"
    elif card_len == 16 and re.match("^5[1-5]", card_number):    
        return "MASTERCARD"
    elif (card_len == 16 or card_len == 13) and re.match("^4", card_number):
        return "VISA"    
    else:
        return "INVALID"  
          

# Luhn's algorithm to validate credit card number
def luhnCheckCard(card_number):
    checksum = 0
    card_len = len(card_number)

    # calculate checksum
    for i in range(card_len):
        digit = int(card_number[card_len - i - 1])
        # Double every second digit and add it to sum 
        if (i + 1) % 2 == 0:
            digit *= 2

        # This will handle cases, if doubling digit produces two digits
        checksum += digit // 10
        checksum += digit % 10

    # Check if checksum ends with 0
    if checksum % 10 == 0:
        return True
    else:
        return False


def validateCardNumber(card_number, card_type):
    if validateCardPattern(card_number):
        if luhnCheckCard(card_number):
            if cardType(card_number) == card_type:
                return True

    # Invalid card number and / or type
    return False 