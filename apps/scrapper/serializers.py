from rest_framework import serializers
from .models import ExchangeRates

class ExchangeRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRates
        fields = ['date', 'open_rate', 'high_rate', 'low_rate', 'close_rate', 'adj_close_rate']
