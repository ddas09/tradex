import sqlite3, os, sys

# Appending root folder to path
sys.path.append(os.getcwd())

from stocks.requests import sendApiRequest

# Accquire connection to the database
connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()


# Get stock list registered on IEX
stocks = sendApiRequest("ref-data/symbols?filter=symbol,name,type, isEnabled&" , sandbox_request = False)
allowed_stock_types = ['ad', 'cs', 'ps']

# Insert new stock informations
query = "INSERT INTO stocks(symbol, name, type) VALUES(?, ?, ?)"
for stock in stocks:
    # Stocks is tradable and in allowed types
    if stock['type'] in allowed_stock_types and stock['isEnabled']:
        try:
            cursor.execute(query, [stock['symbol'], stock['name'], stock['type']])
            print(f"Inserted a new stock: {stock['symbol']}, {stock['name']}")

        except Exception:
            continue


# Close connection
connection.commit()
connection.close()


