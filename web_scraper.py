from bs4 import BeautifulSoup
import requests
import time
import psycopg2
import smtplib

import config

TABLE_NAME = "PRICE_ALERT"

CREATE_QUERY = f""" CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        ID SERIAL PRIMARY KEY,
                        DATE DATE NOT NULL DEFAULT CURRENT_DATE,
                        AD_ID VARCHAR (100),
                        PRICE INTEGER NOT NULL
                )"""


def read_urls():
    urls = {}
    with open('urls.txt', 'r') as file:
        for data in file:
            data = data.rstrip().split("|")
            urls[data[0]] = int(data[1])
    return urls


def send_email(url, price):
    user = config.EMAIL
    password = config.PASSWORD
    to = config.TO
    subject = "PRICE ALERT"
    text = f"{url}\nPrice has been reduced to: {price}"

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(user, password)
        message = f"Subject: {subject} \n\n {text}"
        server.sendmail(user, to, message)
        server.quit()
        print("Alert has been sent")
    except Exception as error:
        print("ERROR. CAN'T SEND ALERT", error)


def execute(query):
    try:
        connection = psycopg2.connect(config.DATA_TO_CONNECT)
        cursor = connection.cursor()
        cursor.execute(query)
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
    else:
        connection.commit()
        cursor.close()
        connection.close()


def find_id(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        ad_id = int(soup.find(id="ad_id").text)
    except Exception as error:
        raise error
    else:
        return ad_id


def find_price(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find(class_="offer-price__number")
        price = str(price.contents[0])
        price = price.split(" ")
        price = int(price[0] + price[1])
    except Exception as error:
        raise error
    else:
        return price


if __name__ == "__main__":
    execute(CREATE_QUERY)
    urls = read_urls()

    while True:
        for url, price_alert in list(urls.items()):
            response = requests.get(url)

            try:
                if response.status_code == 200:
                    ad_id = find_id(response)
                    price = find_price(response)

                    insert_query = f""" INSERT INTO {TABLE_NAME} VALUES (default, default, {ad_id}, {price})"""
                    execute(insert_query)

                    print(price)

                    if price <= price_alert:
                        send_email(url, price)

                    response.close()
                elif response.status_code == 404:
                    urls.pop(url)
                    print("The advertisement is out of date")
                else:
                    print('Connection to the website failed')
            except Exception as error:
                print('Error:', error)

        if not urls:
            print("Urls.txt has not active links. Add links to ad")
            break

        time.sleep(10)  # time in second between downloading data (86400 = 24h)
