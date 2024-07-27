from datetime import datetime,timedelta

import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from django.conf import settings
from django.apps import apps
from django.db import IntegrityError
from structlog import get_logger

from .models import CurrencyExchange,ExchangeRates

logger = get_logger(scrapper='service.py')


def get_exchange_rate_model(currency_pair):
    model_name = f"ExchangeRate{currency_pair.from_currency.code}{currency_pair.to_currency.code}"
    return apps.get_model('scrapper', model_name)


def scrap_exchange_rates(exchangeCurr):
    try:
        end_date    = datetime.now()
        start_date  = end_date - timedelta(days=10000)
        period1 = int(start_date.timestamp())
        period2 = int(end_date.timestamp())
        url = f"https://finance.yahoo.com/quote/{exchangeCurr.getYahooExchSymbol()}/history/?period1={period1}&period2={period2}"
        
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        page_content = response.text
        doc = BeautifulSoup(page_content, 'html.parser')
        tr_tags = doc.find_all('tr', class_='yf-ewueuo')

        if len(tr_tags) == 2:  # Check if there's only the header row or less
                td = doc.find('td', class_='error')
                if td:
                    text = td.text.strip()
                    if "There are no" in text:
                        print("No more data to crawl")
                        return
                    
        for tr in tr_tags[1:]:  # skip the header row
            tds = tr.find_all('td')
            if len(tds) == 7: 
                date            = datetime.strptime(tds[0].text, '%b %d, %Y').date()
                open_rate       = float(tds[1].text.replace(',', ''))
                high_rate       = float(tds[2].text.replace(',', ''))
                low_rate        = float(tds[3].text.replace(',', ''))
                close_rate      = float(tds[4].text.replace(',', ''))
                adj_close_rate  = float(tds[5].text.replace(',', ''))

                try:
                    ExchangeRates.objects.create(
                        currency_exchange=exchangeCurr,
                        date=date,
                        open_rate=open_rate,
                        high_rate=high_rate,
                        low_rate=low_rate,
                        close_rate=close_rate,
                        adj_close_rate=adj_close_rate
                    )
                    logger.info(f"Added data for {exchangeCurr} for {date}")
                except IntegrityError:
                    logger.info(f"Data for {exchangeCurr} on {date} already exists, skipping.")
    except Exception as e:
        logger.error("Something went wrong in scrap_exchange_rates",currency_pair=exchangeCurr,e=str(e))
        raise("Unsuccessful scrapping data")


def run_scraper():
    active_pairs = CurrencyExchange.objects.all()
    for pair in active_pairs:
            scrap_exchange_rates(pair)