from django.template import Library

register = Library()

@register.filter(name="get_price")
def get_price(prices, symbol):
    price = prices[symbol]["price"]
    return price