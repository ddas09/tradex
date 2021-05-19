# TradeX - Full stack django trading app

**Environment:** Django, Python, HTML, CSS, Javascript

## About
It allows users to buy, sell and quote stocks with charting real time stock
market data provided by [IEX Cloud API](https://iexcloud.io/). For charting stock data,
I've used the embeded chart widget of [TradingView](https://in.tradingview.com/).
The idea of the project relies upon the [Week 9: Finance](https://cs50.harvard.edu/x/2021/psets/9/finance/) 
problem set of CS50. 

### To run the application:
Use `python3 manage.py runserver` command from the root directory of the project.

### Popular Routes
`/`
The index route contains a `bootstrap carousel` that shows all the customer reviews
on the home page.

`user/portfolio`
This route shows all the stocks that the user currently own and also their transaction
statistics and current balance.

`/user/stocks`
This route shows all the stock symbols available for trading on a table. The table is spawned on multiple
pages by the use of [Django Paginator](https://docs.djangoproject.com/en/3.2/topics/pagination/).
This page also contains a filter to show a specific type of stocks from the table.

`/user/stocks/quote`, `/user/stocks/buy` and `/user/stocks/sell`
These routes allow users to quote, buy and sell stock shares respectively.

`user/stocks/price/<symbol>`
This route displays the historical price data for the stock whose symbol is passed to the
view. It also shows a chart with the last 15yrs historical price of the stock and also
allows users to customize the chart according to their need.

`user/transaction/history`
All the transaction history of the user is displayed on this page.

## Resources
- All stock market informations are provided by the [IEX Cloud API](https://iexcloud.io/).
- The stock chart widget is taken from [TradingView](https://in.tradingview.com/)'s website.
- Last but not the least, the core idea of the project has been leveraged from 
[Week 9: Finance](https://cs50.harvard.edu/x/2021/psets/9/finance/) problem set of CS50.