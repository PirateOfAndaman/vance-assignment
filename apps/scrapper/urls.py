from django.urls import include, path
from . import views

urlpatterns =[
    path('trigger-scrapper',views.TriggerScrapper.as_view()),
    path('forex-data',views.ExchangeRatesView.as_view()),
]