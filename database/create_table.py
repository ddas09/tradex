import sqlite3

connection = sqlite3.connect("stocks.sqlite3")
cursor = connection.cursor()


query = '''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL UNIQUE,
    email VARCHAR(256) NOT NULL UNIQUE,
    hashed TEXT NOT NULL,
    card_number VARCHAR(16) NOT NULL UNIQUE,
    plan_type CHAR(1) NOT NULL,
    balance NUMERIC NOT NULL,
    check(plan_type in ('S','P','E'))
)'''
cursor.execute(query)


query = '''CREATE TABLE IF NOT EXISTS feedbacks (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    email VARCHAR(256) NOT NULL UNIQUE,
    message VARCHAR(351) NOT NULL,
    approved CHAR(1) NOT NULL DEFAULT 'N',
    time DEFAULT CURRENT_TIMESTAMP NOT NULL,
    check(approved in ('Y','N'))
)'''
cursor.execute(query)


query = '''CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    check(type in ('ad','cs', 'ps'))
)'''
cursor.execute(query)


query = '''CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    date DEFAULT CURRENT_TIMESTAMP NOT NULL,
    type TEXT NOT NULL,
    check (type in ('B', 'S')),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(stock_id) REFERENCES stocks(id)
)'''
cursor.execute(query)


query = '''CREATE TABLE IF NOT EXISTS portfolios (
    user_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    shares_owned INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(stock_id) REFERENCES stocks(id)
)'''
cursor.execute(query)

connection.commit()
connection.close()