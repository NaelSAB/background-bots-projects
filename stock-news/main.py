import requests
import smtplib
import os
from dotenv import load_dotenv
import schedule


load_dotenv()
API_KEY_STOCK = os.getenv("API_KEY_STOCK")
API_KEY_NEWS  = os.getenv("API_KEY_NEWS")
MY_EMAIL      = os.getenv("MY_EMAIL")
MY_PASSWORD   = os.getenv("MY_PASSWORD")
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"




parameter_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCK
}
parameter_news = {
    "apiKey": API_KEY_NEWS,
    "qInTitle": COMPANY_NAME,
}



def job():
    response = requests.get(url=STOCK_ENDPOINT, params=parameter_stock)
    response.raise_for_status()
    data_stock = response.json()["Time Series (Daily)"]
    data_list_stock = [value for (key, value) in data_stock.items()]

    data_yesterday = data_list_stock[0]
    yesterday_closing_price = data_yesterday["4. close"]

    data_bf_yesterday = data_list_stock[1]
    bf_yesterday_closing_price = data_bf_yesterday["4. close"]

    difference_price = float(yesterday_closing_price) - float(bf_yesterday_closing_price)
    up_down = None
    if difference_price > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    difference_price_pct = round(difference_price / float(bf_yesterday_closing_price) * 100)

    if abs(difference_price_pct) > 5:
        print("get News")


        response = requests.get(url=NEWS_ENDPOINT, params=parameter_news)
        response.raise_for_status()
        data_news = response.json()["articles"][:3]

        formatted_article = [f"Subject: {STOCK}: {up_down}{difference_price_pct} - {data['title']}. \n\n{data['description']}" for data in data_news]
        for article in formatted_article:
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=article
            )

schedule.every().day.at("09:00").run(job)

while True:
    schedule.run_pending()
    time.sleep(60)