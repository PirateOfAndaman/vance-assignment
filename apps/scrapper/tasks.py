from datetime import timedelta

from finance.celery_manager import celery_app
from celery import shared_task
from celery.schedules import crontab
from structlog import get_logger

from .service import scrap_exchange_rates 
from .models import Currency,CurrencyExchange

logger = get_logger(scrapper='tasks.py')

celery_app.conf.beat_schedule = {
    'run-scrapper_GBP_INR': {
        'task': 'apps.scrapper.tasks.run_scraper_GBP_INR_task',
        'schedule': timedelta(days=7),  
    },
    'run_scrapper_AED_INR':{
         'task': 'apps.scrapper.tasks.run_scraper_AED_INR_task',
        'schedule': timedelta(days=7),
    }
}
celery_app.conf.timezone='UTC'


@shared_task
def run_scraper_GBP_INR_task():
    try:
        from_curr = Currency.objects.get(code='GBP')
        to_curr   = Currency.objects.get(code = 'INR')
        curr_exch = CurrencyExchange.objects.get(from_currency=from_curr,to_currency=to_curr)
        scrap_exchange_rates(curr_exch,days=7)
    except Exception as e:
        logger.error("Something went wrong in run_scraper_GBP_INR_task",e = str(e))
    

@shared_task
def run_scraper_AED_INR_task():
    try:
        from_curr = Currency.objects.get(code='AED')
        to_curr   = Currency.objects.get(code = 'INR')
        curr_exch = CurrencyExchange.objects.get(from_currency=from_curr,to_currency=to_curr)
        scrap_exchange_rates(curr_exch,days=7)
    except Exception as e:
        logger.error("Something went wrong in run_scraper_AED_INR_task",e = str(e))