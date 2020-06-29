import requests, time, psycopg2
from bs4 import BeautifulSoup

DATA_TO_CONNECT = """
            user='postgres'
            password='12345'
            host='127.0.0.1'
            port='5432'
            dbname='test' 
"""
TABLE_NAME = "PRICE_ALERT"

CREATE_QUERY = f""" CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        ID SERIAL PRIMARY KEY,
                        DATE DATE NOT NULL DEFAULT CURRENT_DATE,
                        AD_ID VARCHAR (100),
                        PRICE INTEGER NOT NULL
    )"""


urls = []
with open('urls.txt', 'r') as file:
    for url in file:
        urls.append(url.rstrip())


def execute(query):
    try:
        connection = psycopg2.connect(DATA_TO_CONNECT)
    except (Exception, psycopg2.Error) as error:
        print("Connecting Error", error)
        connection = None

    cursor = connection.cursor()

    try:
        cursor.execute(query)
    except (Exception, psycopg2.Error) as error:
        print("Execute query Error", error)
        connection = None

    finally:
        connection.commit()
        if connection != None:
            cursor.close()
            connection.close()


def find_price():
    while True:
        for url in urls:
            response = requests.get(url)
            try:
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    ad_id = int(soup.find(id="ad_id").text)

                    price = soup.find(class_="offer-price__number")
                    price = str(price.contents[0])
                    price = price.split(" ")
                    price = int(price[0] + price[1])

                    insert_query = f""" INSERT INTO {TABLE_NAME} VALUES (default, default, {ad_id}, {price})"""
                    print(price)
                    execute(insert_query)
                    response.close()
                else:
                    print('Connection to the website failed')
            except:
                print('Error')

        time.sleep(2)  # time in second between downloading data (86400 = 24h)


execute(CREATE_QUERY)
find_price()
