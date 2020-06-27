import requests, time, psycopg2
from bs4 import BeautifulSoup


URL = "https://www.otomoto.pl/oferta/peugeot-308-ID6DbgVh.html?"
response = requests.get(URL)

try:
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        while True:
            results = soup.find(class_="offer-price__number")
            results = str(results.contents[0])
            results = results.split(" ")
            results = int(results[0] + results[1])
            print(results)
            time.sleep(10) #time in second between downloading data
    else:
        print('Connection failed')
except:
    print('Error')
