import requests
from requests import Session
import datetime
from twilio.rest import Client
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# stocks api parameters
STOCKS_ENDPOINT = "https://www.alphavantage.co/query"
STOCKS_API_KEY = 'YOUR API-KEY HERE'

# crypto tracking api parameters
CRYPTO_ENDPOINT = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
CRYPTO_API_KEY = 'YOUR API-KEY2 HERE'

# news api parameters
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = 'YOUR API-KEY3 HERE'

# twilio api parameters
ACCOUNT_SID = 'YOUR ACCOUNT SID HERE'
AUTH_TOKEN = 'YOUR AUTHENTICATION TOKEN HERE'

STOCK_PARAMETERS = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'outputsize': 'compact',
    'apikey': STOCKS_API_KEY
}

CRYPTO_PARAMETERS = {
    'id': '1',
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CRYPTO_API_KEY,
}

NEWS_PARAMETERS = {
    'apiKey': NEWS_API_KEY,
    'q': COMPANY_NAME,
    'searchIn': 'title,content',
    'from': str(datetime.date.today() - datetime.timedelta(days=2)),
    'to': str(datetime.date.today()),
    'language': 'en',
    'sortBy': "relevancy",
}

# Get stock data with error handling
try:
    stocks_response = requests.get(url=STOCKS_ENDPOINT, params=STOCK_PARAMETERS)
    stocks_response.raise_for_status()
    tsla_stock_data = stocks_response.json()
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print("Error getting stock data:", e)
    tsla_stock_data = None

# Cryptocurrency API settings
session = Session()
session.headers.update(headers)

# Initialize variables
crypto_data = None
price = None
percent_change_24h = None

try:
    crypto_response = session.get(url=CRYPTO_ENDPOINT, params=CRYPTO_PARAMETERS)
    crypto_response.raise_for_status()
    crypto_data = crypto_response.json()
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print("Erro ao obter dados da criptomoeda:", e)
    crypto_data = None

# Process crypto data
if crypto_data:
    try:
        quote = crypto_data.get('data', {}).get('1', {}).get('quote', {}).get('USD', {})  # '1' = Bitcoin
        price = quote['price']
        percent_change_24h = quote['percent_change_24h']
    except (KeyError, TypeError) as e:
        print("Error processing crypto data:", e)
        price = None
        percent_change_24h = None

# Send crypto alert if significant change
if percent_change_24h is not None and abs(percent_change_24h) > 7:
    up_down = '🔺' if percent_change_24h > 0 else '🔻'
    now = datetime.now().strftime('%Y-%m-%d')
    formatted_msg = f"BTC:(in {now})\n{up_down}{abs(round(percent_change_24h, 1))}%\nPrice: ${round(price, 2)}"

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+5511981704765',
            body=formatted_msg
        )
        print(message.sid)
    except Exception as e:
        print("Error sending crypto message:", e)

# Process stock data
if tsla_stock_data is not None:
    dates = sorted(tsla_stock_data['Time Series (Daily)'].keys(), reverse=True)

    try:
        most_recent = dates[0]
        price_most_recent = float(tsla_stock_data['Time Series (Daily)'][most_recent]['4. close'])
        previous = dates[1]
        price_previous = float(tsla_stock_data['Time Series (Daily)'][previous]['4. close'])

    except (KeyError, IndexError) as e:
        print("Insufficient data to calculate the price:", e)
        price_most_recent = None
        price_previous = None

    # Calculate percentage difference
    if price_most_recent is not None and price_previous is not None and price_most_recent != 0:
        dif_price = price_most_recent - price_previous
        up_down = '🔺' if dif_price > 0 else '🔻'
        percentual_dif_price = round((dif_price / price_previous) * 100, 1)

        if abs(percentual_dif_price) > 5:
            try:
                news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
                news_response.raise_for_status()
                news_data = news_response.json()

                # Get first 3 articles
                articles = news_data['articles'][:3]

                # Create formatted articles
                lean_articles = [
                    f'{STOCK_NAME}: {up_down}{abs(percentual_dif_price)}%\nHeadline: {art["title"]}\nBrief: {art["description"]}'
                    for art in articles]

                # Send each article as a separate message via Twilio
                client = Client(ACCOUNT_SID, AUTH_TOKEN)

                for article in lean_articles:
                    message = client.messages.create(
                        from_='whatsapp: THE NUMBER GIVEN IN TWILIO',
                        to='whatsapp: A WHATSAPP NUMBER',
                        body=article,
                    )
                print(message.sid)

            except Exception as e:
                print("Error getting or sending news:", e)
    else:
        print("Cannot calculate percentage difference - invalid price data")
