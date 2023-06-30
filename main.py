import requests
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
api_key = "CP0LNPCPSEI0C4EO"

api_key_news = "418d10c6357644818dce2214462ba3b1"


stock_params = {"function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": STOCK,
                "apikey": api_key
                }
response = requests.get(STOCK_ENDPOINT, params=stock_params)

data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_data_closing_price = yesterday_data['4. close']

day_before_data = data_list[1]
day_before_data_closing_price = day_before_data['4. close']


difference = abs(float(yesterday_data_closing_price) -
                 float(day_before_data_closing_price))

diff_percent = (difference/float(yesterday_data_closing_price))*100
print(diff_percent)

news_params = {"apikey": api_key_news,
               "q": COMPANY_NAME}
if diff_percent > 4:
    print("hi")
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response.json()['articles'][:3]
    # three_articles = articles[:3]
    # print(three_articles)
    articles_only = [
        f"Headline: {article['title']}, \nBrief: {article['description']}" for article in articles]

    import os
    from twilio.rest import Client

    TWILIO_ACCOUNT_STD = "AC2bdf96451a39c3207a1e738c49b7029d"
    TWILIO_AUTH_TOKEN = "c528f2e5039ea0634d7a83fd2ac9e081"
    client = Client(TWILIO_ACCOUNT_STD, TWILIO_AUTH_TOKEN)

    for article in articles_only:
        message = client.messages .create(
            body=article,
            from_='+14175578223',
            to='+919391469517'
        )
    print("SMS sent successfully")
else:
    print("The difference is below 4 so we could'nt sent the SMS")
