from os import stat
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from stocks.decorators import *
from stocks.validations import *
from stocks.queries import *
from stocks.requests import *
from stocks.mails import *
from datetime import datetime, timedelta
from django.core.paginator import Paginator


#  These are views for the navbar pages when user is not logged in
    
def index(request):
    # Fetch customer reviews from database
    reviews = getCustomerReviews()

    # Converting timestamp string to proper format
    for review in reviews:
        review["time"] = datetime.strptime(review["time"], "%Y-%m-%d %H:%M:%S")
        review["time"] = datetime.strftime(review["time"], "%b %d, %Y at %I:%M %p")

    return render(request, "webnav/index.html", {"reviews": reviews})


def about(request):
    return render(request, "webnav/about.html")


def contact(request):
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        feedback_msg = request.POST.get("msg")

        # Validate user details for proper formats
        if not validateName(first_name):
            return JsonResponse({"status": 1, "alertInputId": "#fname", "msg": "Please enter a valid first name"})

        if not validateName(last_name):
            return JsonResponse({"status": 1, "alertInputId": "#lname", "msg": "Please enter a valid last name"})    

        # Validate user's email
        if not validateEmail(email):
            return JsonResponse({"status": 1, "alertInputId": "#mail", "msg": "Please enter a valid email address"})
        
        # Validate feedback length
        feedback_length = len(feedback_msg.strip())
        if feedback_length < 20: 
            return JsonResponse({"status": 1, "alertInputId": "#msg-box", "msg": "Feedback is too short"})
        elif feedback_length > 350:
            return JsonResponse({"status": 1, "alertInputId": "#msg-box", "msg": "Feedback limit is 350 characters"})

        # Insert feedback into db
        registerFeedback(first_name, last_name, email, feedback_msg)
        
        messages.success(request, "Thanks for your feedback! : )")
        return JsonResponse({"status": 0, "redirectUrl": "/contact"})

    else:
        return render(request, "webnav/contact.html")


def pricing(request):
    return render(request, "webnav/pricing.html")        


@not_logged_in
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate username for proper format
        if not validateUsername(username):
            return JsonResponse({"status": 1, "alertInputId": "#username", "msg": "Please provide a valid username"})

        # Check database for user
        user_id = getUserId(username, password)
        if user_id:
            request.session["user_id"] = user_id
            return JsonResponse({"status": 0, "redirectUrl": "/user/portfolio"})
        else:
            return JsonResponse({"status": 1, "alertInputId": "#toggler", "msg": "Invalid username or password"})    

    else:
        return render(request, "webnav/login.html")
          

@not_logged_in
def register(request):
    if request.method == "POST":        
        mail = request.POST.get("mail")

        # Validate user's email
        if not validateEmail(mail):
            return JsonResponse({"status": 1, "alertInputId": "#mail", "msg": "Please enter a valid email address"})

        # Check if email already exists
        if emailExists(mail):
            return JsonResponse({"status": 1, "alertInputId": "#mail", "msg": "This email address is already registered"})
        else:    
            request.session["mail"] = mail
            return JsonResponse({"status": 0, "redirectUrl": "/account/send_otp"})

    else:    
        return render(request, "webnav/register.html")   


''' These are views that renders different forms when a user registers
    These must be wrapped with a decorator to ensure that user can"t
    access these views by manually entering the urls '''

@mail_required
def send_otp(request):
    user_mail = request.session["mail"]

    # Sends an otp to the email that user provided
    otp = sendOTP(user_mail)

    # Store otp for verification
    request.session["otp"] = otp
    return redirect("validate_mail")


@otp_required
def validate_mail(request):
    if request.method == "POST":
        otp_provided = request.POST.get("otp")

        # OTP matched with the one that we mailed user
        if otp_provided == request.session["otp"]:
            request.session["verified"] = True
            user_mail = request.session["mail"]

            # Send mail
            sendMailVerified(user_mail)           
            return JsonResponse({"status": 0, "redirectUrl": "/account/open_account/"})

        # Invalid otp provided
        else:    
            return JsonResponse({"status": 1, "alertInputId": "#otp", "msg": "The otp that you entered is invalid"})
            
    else:
        return render(request, "account/validate_mail.html")  


@mail_validation_required    
def open_account(request):
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        username = request.POST.get("username")

        # Validate user details for proper formats
        if not validateName(first_name):
            return JsonResponse({"status": 1, "alertInputId": "#fname", "msg": "Please enter a valid first name"})

        if not validateName(last_name):
            return JsonResponse({"status": 1, "alertInputId": "#lname", "msg": "Please enter a valid last name"})

        if not validateUsername(username):
            return JsonResponse({"status": 1, "alertInputId": "#username", "msg": "Please enter a valid username"})
        
        # Check if username already exists in database 
        if usernameExists(username):
            return JsonResponse({"status": 1, "alertInputId": "#username", "msg": "This username is taken"})
        else:    
            request.session["first_name"] = first_name
            request.session["last_name"] = last_name
            request.session["username"] = username
            return JsonResponse({"status": 0, "redirectUrl": "/account/create_password/"})

    else:    
        return render(request, "account/open_account.html")


@details_required  
def create_pass(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        # Validate password format 
        if validatePassword(password) and validatePassword(confirm):   
            # Check if passwords match
            if password == confirm:
                request.session["password"] = password
                return JsonResponse({"status": 0, "redirectUrl": "/account/select_plan/"})
            else:
                return JsonResponse({"status": 1, "alertInputId": "#confirm", "msg": "Entered passwords does not match"})
        
        else:        
            return JsonResponse({"status": 1, "alertInputId": "#pass", "msg": "Password does not match all the requirements"})

    else:    
        return render(request, "account/create_pass.html", {"title": "Create a password for your account", "form_id": "create-pass"})


@pass_required  
def select_plan(request):
    if request.method == "POST":
        card_number = request.POST.get("card")
        card_type = request.POST.get("cardtype")
        plan_type = request.POST.get("plantype")
        timeZoneOffset = int(request.POST.get("offset"))

        # Calculate date in end user"s timezone
        date = datetime.now() - timedelta(minutes=timeZoneOffset)

        # Check if card number already exists in database
        if cardExists(card_number):
            return JsonResponse({"status": 1, "alertInputId": "#card", "msg": "This card has already been registerd"}) 

        # Check for proper values and format
        if not validateCardType(card_type):
            return JsonResponse({"status": 1, "alertInputId": "#cardtype", "msg": "Please enter a valid card type from the list"})

        if not validatePlanType(plan_type):
            return JsonResponse({"status": 1, "alertInputId": "#plantype", "msg": "Please enter a valid plan type from the list"})    

        # Validate card(using luhn"s algorithm)
        if validateCardNumber(card_number, card_type):
            request.session["card_number"] = card_number
            request.session["plan_type"] = plan_type
            request.session["timezone_offset"] = timeZoneOffset

            # Insert everything in database
            registerUser(request)

            # Send mail
            sendAccountCreated(request, date)

            # Delete all session data
            request.session.flush()

            return JsonResponse({"status": 0, "redirectUrl": "/login/"})

        # Invalid credit card
        else:
            return JsonResponse({"status": 1, "alertInputId": "#card", "msg": "Invalid credit card number"})

    else:   
        return render(request, "account/select_plan.html", {"title": "Select your plan", "form_id": "select-plan"})
        

''' These are views available to user when user is logged in,
    apply decorator to make sure that user is logged in,
    if not redirect user to login page i.e user tries to access
    page by entering urls manually '''

@login_required
def portfolio(request):
    user_id = request.session["user_id"]
    user = getUserInfo(user_id)
    portfolio = getUserPortfolio(user_id)

    # Get user transaction satistics
    stat = getTransactionStatistics(user_id)
    stock_count = len(portfolio)

    context = {"user": user, "portfolio": portfolio, "count": stock_count, "stat": stat}
    return render(request, "usernav/portfolio.html", context)


@login_required
def stocks(request):
    # The page that user has requested
    try:
        requested_page = int(request.GET.get("page"))
    except Exception:
        requested_page = 1    

    # Get list of stocks from db
    stocks = getAllStockInfo()
    
    # Create a paginator object(it splits the data in pages)
    content = Paginator(stocks, 500)

    # Page is invalid, forward to first page
    if requested_page not in content.page_range:
        requested_page = 1

    # Get the content of requested page
    page_content  = content.page(requested_page)

    # Calculate the page range relative to current page 
    if (requested_page - 2) > 0:
        start = requested_page - 2
    else:
        start = 1

    if (requested_page + 2) < content.num_pages:
        end = requested_page + 2
    else:
        end =  content.num_pages 

    page_range = range(start, end + 1)

    # Pass the custom page range to the template
    context = {"stocks": page_content, "page_range": page_range, "start": start, "end": end}
    return render(request, "usernav/stocks.html", context)


@login_required
def quote(request):
    if request.method == "POST":
        symbol = request.POST.get("symbol")

        # Check if user has provided a valid stock symbol
        stock = getStockInfo(symbol)
        if not stock:
            return JsonResponse({"status": 1, "alertInputId": "#symbol", "msg": "Enter a valid stock symbol"})
        else:
            return JsonResponse({"status": 0, "redirectUrl": f"/user/stocks/price/{symbol.upper()}/"})

    else:
        return render(request, "usernav/quote.html")


@login_required
def price(request, symbol = "AAPL"):
    stock = getStockInfo(symbol)
    if not stock:
        return redirect("stocks")

    historical_price = getHistoricalPrice(symbol)
    return render(request, "usernav/price.html", {"stock": stock, "history": historical_price})


@login_required
def buy(request):
    if request.method == "POST":
        symbol = request.POST.get("symbol")

        # Check if user has provided a valid stock symbol
        stock = getStockInfo(symbol)
        if not stock:
            return JsonResponse({"status": 1, "alertInputId": "#symbol", "msg": "Enter a valid stock symbol"})

        try:
            shares = int(request.POST.get("shares"))
        except Exception:
            shares = 0

        if shares not in range(5, 101):
            return JsonResponse({"status": 1, "alertInputId": "#shares", "msg": "Enter a number between 5 and 100"})        

        stock_price = getStockPrice(symbol)
        total_cost = stock_price * shares

        # Fetch user"s balance
        user_id = request.session["user_id"]
        balance = getUserBalance(user_id)
        
        # Update user balance and add shares to user"s portfolio
        if balance >= total_cost:
            updateUserBalance(user_id, -total_cost)
            recordTransaction(user_id, stock["id"], shares, stock_price, "B")
            updatePortfolio(user_id, stock["id"], shares, "B")
            messages.info(request, f"Successfully bought {shares} share(s) of {stock['name']} ({stock['symbol']})")
            return JsonResponse({"status": 0, "redirectUrl": "/user/stocks/buy/"})
        else:
            return JsonResponse({"status": 1, "alertInputId": "#shares", "msg": "You don't have enough balance to buy these shares"})        
            
    else:
        return render(request, "usernav/buy.html")


@login_required
def sell(request):
    user_id = request.session["user_id"]
    if request.method == "POST":
        symbol = request.POST.get("symbol")

        # check if user owns this stock
        stock = getSharesOwnedByUser(user_id, symbol)
        if not stock:
            return JsonResponse({"status": 1, "alertInputId": "#symbol", "msg": "You don't own this stock"})    
    
        try:
            shares = int(request.POST.get("shares"))
        except Exception:
            shares = 0

        if shares not in range(1, 101):
            return JsonResponse({"status": 1, "alertInputId": "#shares", "msg": "Enter a number between 1 and 100"})
        
        shares_owned = stock["shares_owned"]
        if shares <= shares_owned:
            stock_price = getStockPrice(symbol)
            income = shares * stock_price

            # Sell the shares
            updateUserBalance(user_id, income)
            recordTransaction(user_id, stock["stock_id"], shares, stock_price, "S")
            updatePortfolio(user_id, stock["stock_id"], -shares, "S")
            
            messages.info(request, f"Successfully sold {shares} share(s) of {stock['name']} ({symbol})")
            return JsonResponse({"status": 0, "redirectUrl": "/user/stocks/sell/"})
        else:    
            return JsonResponse({"status": 1, "alertInputId": "#shares", "msg": "You don't own this much shares"})        

    else:
        stocks_owned = getUserPortfolio(user_id)
        return render(request, "usernav/sell.html", {"stocks_owned": stocks_owned})


@login_required
def history(request):
    transaction_history = getTransactionHistory(request.session["user_id"])
    
    # Converting timestamp string to proper format
    for history in transaction_history:
        history["date"] = datetime.strptime(history["date"], "%Y-%m-%d %H:%M:%S")
        history["date"] = datetime.strftime(history["date"], "%d/%m/%Y")

    return render(request, "usernav/history.html", {"transaction_history": transaction_history})


@login_required
def logout(request):
    # Clear session data
    request.session.flush()
    return redirect("login")


@not_logged_in
def confirm_mail(request):
    if request.method == "POST":
        mail = request.POST.get("mail")
        username = request.POST.get("username")

        user = checkUserMail(mail, username)
        if user:
            request.session["user"] = user
            return JsonResponse({"status": 0, "redirectUrl": "/account/change_password/"})
        else:
            return JsonResponse({"status": 1, "alertInputId": "#mail", "msg": "Invalid username or email address"}) 

    else:
        return render(request, "account/confirm_mail.html")


@user_validation_required
def change_password(request):
    if request.method == "POST":
        new_pass = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if not validatePassword(new_pass) or not validatePassword(confirm):  
            return JsonResponse({"status": 1, "alertInputId": "#pass", "msg": "Password does not match all the requirements"})    

        if new_pass == confirm:
            user = request.session["user"]
            if changeUserPassword(user, new_pass):
                messages.info(request, "Your password has been changed")
                request.session.flush()
                return JsonResponse({"status": 0, "redirectUrl": "/login/"})
            else:
                return JsonResponse({"status": 1, "alertInputId": "#confirm", "msg": "New password cannot be same as old"})        
        
        else:
            return JsonResponse({"status": 1, "alertInputId": "#confirm", "msg": "Entered passwords does not match"})

    else:    
        return render(request, "account/create_pass.html", {"title": "change password", "form_id": "change-pass"})







