import requests, time, psycopg2
from bs4 import BeautifulSoup

DATA_TO_CONNECT = """
            user='postgres'
            password='12345'
            host='127.0.0.1'
            port='5432'
            dbname='test1' 
"""
TABLE_NAME = "PRICE_ALERT"

CREATE_QUERY = f""" CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                        ID SERIAL PRIMARY KEY,
                        DATE DATE NOT NULL DEFAULT CURRENT_DATE,
                        PRICE INTEGER NOT NULL
    )"""


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
    URL = "https://www.otomoto.pl/oferta/opel-corsa-c-1-0-ben-klima-5-drzwi-2002-mozliwa-zamiana-zarejestr-ID6CyGmZ.html"
    response = requests.get(URL)

    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            while True:
                results = soup.find(class_="offer-price__number")
                results = str(results.contents[0])
                results = results.split(" ")
                results = int(results[0] + results[1])
                insert_query = f""" INSERT INTO {TABLE_NAME} VALUES (default, default, {results})"""
                print(results)
                execute(insert_query)
                time.sleep(86400)  # time in second between downloading data (86400 = 24h)
        else:
            print('Connection to the website failed')
    except:
        print('Error')


execute(CREATE_QUERY)
find_price()
