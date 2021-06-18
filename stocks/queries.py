from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
from re import split

# Provides functions to query database

# Strip stock name to fit table
def stripStockName(name):
    return split("\.|-|\s-", name)[0]


# Returns all rows from a cursor as a dictionary
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]

    # Make a dictionary of the query result set
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results


# Executes a query on the database connection
def executeQuery(query, args = None):
    with connection.cursor() as cursor:
        cursor.execute(query, args)

        # If it's a retrieval query 
        if cursor.description:
            return dictfetchall(cursor)


def getTransactionStatistics(user_id):
    stat = {}
    result = executeQuery("SELECT SUM(price * quantity) AS total FROM transactions WHERE user_id = %s AND type = 'B'", [user_id])
    stat["bought"] = round(result[0]["total"], 2) if result[0]["total"] else 0

    result = executeQuery("SELECT SUM(price * quantity) AS total FROM transactions WHERE user_id = %s AND type = 'S'", [user_id])
    stat["sold"] = round(result[0]["total"], 2) if result[0]["total"] else 0

    return stat


def getUserInfo(user_id):
    user_info = executeQuery("SELECT first_name, plan_type, balance FROM users WHERE id = %s", [user_id])
    user_info[0]["balance"] = round(user_info[0]["balance"], 2)
    return user_info[0]


def changeUserPassword(user_id, new_pass):
    rows = executeQuery("SELECT hashed FROM users WHERE id = %s", [user_id])
    old_pass = rows[0]["hashed"]
    
    if check_password(new_pass, old_pass):
        return False
    else:
        hashed_pass = make_password(new_pass)
        executeQuery("UPDATE users SET hashed = %s WHERE id = %s", [hashed_pass, user_id])
        return True


def checkUserMail(mail, username):
    rows = executeQuery("SELECT id FROM users WHERE email = %s AND username = %s", [mail, username])
    return rows[0]['id'] if rows else rows
    

def getSharesOwnedByUser(user_id, symbol):
    query = '''SELECT stock_id, name, shares_owned FROM portfolios JOIN stocks ON stocks.id = portfolios.stock_id
    WHERE user_id = %s AND symbol = %s'''
    result = executeQuery(query, [user_id, symbol])

    if result:
        result[0]['name'] = stripStockName(result[0]['name'])
        return result[0]
    else:
        return None    


def getUserPortfolio(user_id):
    query = "SELECT symbol, shares_owned, name FROM portfolios JOIN stocks ON stocks.id = portfolios.stock_id WHERE user_id = %s"
    stocks_owned = executeQuery(query, [user_id])
    return stocks_owned


def updateUserBalance(user_id, cost):
    executeQuery("UPDATE users SET balance = balance + %s WHERE id = %s", [cost, user_id])


def recordTransaction(user_id, stock_id, quantity, price, transaction_type):
    query = "INSERT INTO transactions (user_id, stock_id, quantity, price, type) VALUES (%s, %s, %s, %s, %s)"
    executeQuery(query, [user_id, stock_id, quantity, price, transaction_type])


def updatePortfolio(user_id, stock_id, shares, transaction_type):
    result = executeQuery("SELECT * FROM portfolios WHERE user_id = %s AND stock_id = %s", [user_id, stock_id])
    
    if result:
        query = "UPDATE portfolios SET shares_owned = shares_owned + %s WHERE user_id = %s AND stock_id = %s"
        executeQuery(query, [shares, user_id, stock_id])
    else:
        executeQuery("INSERT INTO portfolios (user_id, stock_id, shares_owned) VALUES (%s, %s, %s)", [user_id, stock_id, shares])

    # Remove stocks that user doesn't own anymore
    if transaction_type == 'S':
        executeQuery("DELETE FROM portfolios WHERE shares_owned = 0")


def getUserBalance(user_id):
    result = executeQuery("SELECT balance FROM users WHERE id = %s", [user_id])
    return result[0]['balance']


def getTransactionHistory(user_id):
    query = '''SELECT date, symbol, name, quantity, price, transactions.type FROM transactions 
    JOIN stocks ON transactions.stock_id = stocks.id WHERE user_id = %s'''
    transactions = executeQuery(query, [user_id])

    if transactions:
        for transaction in transactions:
            transaction['name'] = stripStockName(transaction['name'])  

    return transactions


def getStockInfo(symbol):
    result = executeQuery("SELECT id, symbol, name FROM stocks WHERE symbol = %s", [symbol.upper()])

    if result:
        result[0]['name'] = stripStockName(result[0]['name'])
        return result[0]
    else:
        return None


def getAllStockInfo():
    stocks = executeQuery("SELECT * FROM stocks")

    if stocks:
        for stock in stocks:
            stock['name'] = stripStockName(stock['name'])

        return stocks
    else:
        return None


def getCustomerReviews():
    reviews = executeQuery("SELECT id, first_name, last_name, message, time FROM feedbacks WHERE approved = 'Y' Limit 6")
    return reviews

    
def emailExists(mail):
    is_registered = executeQuery("SELECT id FROM users WHERE email = %s", [mail])

    if is_registered:
        return True
    else:
        return False    


def usernameExists(username):
    username_exists = executeQuery("SELECT id FROM users WHERE username = %s", [username])

    if username_exists:
        return True
    else:
        return False  


def cardExists(card_number):
    card_exists = executeQuery("SELECT id FROM users WHERE card_number = %s", [card_number])

    if card_exists:
        return True
    else:
        return False


def getUserId(username, password):
    user = executeQuery("SELECT id, hashed FROM users WHERE username = %s", [username])

    # Check if hashed passwords match
    if user and check_password(password, user[0]['hashed']):
        return user[0]['id']    
    else:
        return False    


def planOpeningBalance(plan):
    if plan == "S":
        return 15000
    elif plan == "P":
        return 30000
    elif plan == "E":
        return 60000    


def registerUser(request):
    # Get data from session
    fname = request.session['first_name']
    lname = request.session['last_name']
    username = request.session['username']
    mail = request.session['mail']
    card_number = request.session['card_number']
    plan_type = request.session['plan_type'][0]

    # Balance according to plan
    balance = planOpeningBalance(plan_type)

    # Hash user's password 
    hashed_pass = make_password(request.session['password'])

    query = '''INSERT INTO users 
    (first_name, last_name, username, email, hashed, card_number, plan_type, balance)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''' 

    executeQuery(query, [fname, lname, username, mail, hashed_pass, card_number, plan_type, balance])


def registerFeedback(fname, lname, mail, feedback_msg):
    user_has_feedback = executeQuery("SELECT id FROM feedbacks WHERE email = %s", [mail])  

    # Update user's feedback
    if user_has_feedback:
        executeQuery("UPDATE feedbacks SET message = %s WHERE email = %s", [feedback_msg, mail])        
    else:
        query = "INSERT INTO feedbacks (first_name, last_name, email, message) VALUES (%s, %s, %s, %s)"
        executeQuery(query, [fname, lname, mail, feedback_msg])

        
          