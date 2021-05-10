# TradeX - Online Trading Platform

**Environment:** Django,  Python, HTML, CSS, Javascript

## About
For my CS50 final project, I've built a full stack trading web app using Django.
It allows users to buy, sell and quote stocks with charting real time stock
market data provided by [IEX Cloud API] (https://iexcloud.io/). For charting data,
I've used the embeded chart widgets of [TradingView] (https://in.tradingview.com/).
The idea of the project relies upon the [Week 9: Finance] (https://cs50.harvard.edu/x/2021/psets/9/finance/)
problem set of CS50. But I've managed to enhance the project by leveraging ideas taught
in the course and implementing some unique features that not makes the application
aesthetically pleasant but also improves the security of it.

### To run the application:
Use `python manage.py runserver` command from the route directory of the project.

### Routes
`/`
The index route contains a `bootstrap carousel` that shows all the customer reviews
on the home page.

`/about`
As the name suggests, this route contains the informations about the people behind
this project, whoever has contributed to this project with their ideas.

`/contact`
The contact route allows users to send a message through the contact form. It also
displays the social handles of the company.

`user/portfolio`
This route shows all the stocks that the user currently own and also their transaction
statistics and current balance.

`/user/stocks`
This route shows all the available stock symbols on a table. The table is spawned on multiple
pages by the use of [Django Paginator] (https://docs.djangoproject.com/en/3.2/topics/pagination/).
This page also contains a filter to show a specific type of stock from the table.

`/user/stocks/quote`, `/user/stocks/buy` and `/user/stocks/sell`
These routes allow users to quote, buy and sell shares respectively.

`user/stocks/price/<symbol>`
This routes displays the historical price of the stocks whoes symbol is passed to the
view. It also shows a chart with the last 15yrs price data of the stock and also
allows users to customize the chart according to their need.

`user/transaction/history`
All the transaction history of the user is displayed on this page.

### Highlights
- I've tried to make the whole application as much responsive as I could using css
media queries and bootstrap classes.
- I've also implemented a mobile friendly navbar and responsive footer on the project.
- Security is maintained while keeping in mind the user friendliness of the application
by using AJAX form submissions.

## Resources
- All the financial market informations are provided by the [IEX Cloud API] (https://iexcloud.io/),
that we've used on the course.
- The beautiful stock chart widgets are borrowed from [TradingView]'s (https://in.tradingview.com/) website.
- The pictures for the carousel item on the home page is taken from [Pixel]'s (https://www.pexels.com/search/people/)
website.
- Some code snippets written by exprienced developers have been taken from [Stackoverflow] (https://stackoverflow.com/).
- Last but not the least, the core idea of the project has been leveraged from [Week 9: Finance]
(https://cs50.harvard.edu/x/2021/psets/9/finance/) problem set of CS50.