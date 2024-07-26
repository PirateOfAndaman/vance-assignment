from finance.celery_manager import celery_app
from celery import shared_task
from .service import scrap_exchange_rates 
from .models import Currency,CurrencyExchange


CURR_PAIRS ={
    ('GBP','INR'),
    ('AED','INR')
}

@shared_task
def run_scraper_GBP_INR_task():
    from_curr = Currency.objects.get(code='GBP')
    to_curr   = Currency.objects.get(code = 'INR')
    curr_exch = CurrencyExchange.objects.get(from_currency=from_curr,to_currency=to_curr)
    scrap_exchange_rates(curr_exch,days=1)
    

@shared_task
def run_scraper_AED_INR_task():
    from_curr = Currency.objects.get(code='AED')
    to_curr   = Currency.objects.get(code = 'INR')
    curr_exch = CurrencyExchange.objects.get(from_currency=from_curr,to_currency=to_curr)
    scrap_exchange_rates(curr_exch,days=1)
    