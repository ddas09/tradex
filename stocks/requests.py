from dotenv import load_dotenv
import os, requests 

# Loads environment variables from .env file
load_dotenv()


# Provides functions to send API requests to IEX Cloud
def sendApiRequest(raw_url, sandbox_request = True):
    '''If sandbox_request is False, it will use production url for API calls
    Visit IEX Cloud website @https://iexcloud.io/docs/api/ for more details'''

    if sandbox_request:
        base_url = os.getenv("IEX_API_SANDBOX_BASE_URL")
        api_token = "token=" + os.getenv("IEX_API_SANDBOX_TOKEN")
    else:
        base_url = os.getenv("IEX_API_BASE_URL")
        api_token = "token=" + os.getenv("IEX_API_TOKEN")

    # Calling API
    try:
        request_url = base_url + raw_url + api_token
        response = requests.get(request_url)
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.HTTPError as error:
        print (error)
        results = None

    return results


def getHistoricalPrice(symbol):
    raw_url = f"stock/{symbol}/chart/6m?filter=close,high,low,open,volume,date&"    
    price_history = sendApiRequest(raw_url)
    return price_history


def getStockPrice(symbol):
    price = sendApiRequest(f"stock/{symbol}/price?")
    return price
