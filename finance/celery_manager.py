import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')
celery_app = Celery('finance-worker')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

celery_app.conf.beat_schedule = {
    'run-scrapper_GBP_INR': {
        'task': 'apps.scrapper.tasks.run_scraper_GBP_INR_task',
        'schedule': crontab(minute='*'),  # Every hour
    },
    'run_scrapper_AED_INR':{
         'task': 'apps.scrapper.tasks.run_scraper_AED_INR_task',
        'schedule': crontab(minute='*'),
    }
}
celery_app.conf.timezone='UTC'
