# Web scraper app to otomoto.pl
> App to monitoring ad from otomoto.pl website. If the price is reduced bellow certain value, the application will send information via email message.
> In addition app connects to postgreSQL database and save price so you can analyze price changes.

## Table of contents
* [Requirements](#requirements)
* [Install](#install)
* [Add ad to track and define price](#add_ad)
* [Connect to database and gmail account](#connect_to)

## Requirements
* Python3
* PostgreSQL

## Install 
* Create virtual environment and activate it
```
$: virtualenv venv
$: source venv/bin/activate
```

* Clone git repository
```
$: git clone https://github.com/karol6112/webscraper.git
```

* Install requirements
```
$: pip install -r requirements.txt
```

## Add ad to track and define price
In urls.txt file add url to ad from otomoto.pl and price to alert. For example:
```
your_url|price
https://www.otomoto.pl/oferta/opel-corsa-1-0-benzyna-super|3500
```

## Connect to database and gmail account
* Set up config.py from config.template. 
* In config.py add data necessary to connect to PostgreSQL database and Gmail account, which app use to send the Price Alert.
* You must allow access to a less secure application on your Gmail account: <br>
https://myaccount.google.com/lesssecureapps