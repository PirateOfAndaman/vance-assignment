import urllib.parse

from django.db import models
from django.core.exceptions import ValidationError

from common.helpers import BaseModelMixin


class Currency(BaseModelMixin):
    class Meta:
        db_table = 'currency'
        
    CURRENCY_CHOICES = {
        'USD': 'United States Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound Sterling',
        'JPY': 'Japanese Yen',
        'AUD': 'Australian Dollar',
        'CAD': 'Canadian Dollar',
        'CHF': 'Swiss Franc',
        'CNY': 'Chinese Yuan',
        'INR': 'Indian Rupee',
        'AED': 'United Arab Emirates Dirham',
        # more currencies as needed
    }
        
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    
    def clean(self):
        if self.code not in self.CURRENCY_CHOICES:
            raise ValidationError(f"'{self.code}' is not a valid currency code.")
        if self.name != self.CURRENCY_CHOICES[self.code]:
            raise ValidationError(f"Currency name does not match the predefined name for '{self.code}'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"


class CurrencyExchange(BaseModelMixin):
    class Meta:
        db_table = 'currency_exchange'
        unique_together = ['from_currency','to_currency']
    from_currency       = models.ForeignKey(Currency, on_delete=models.CASCADE,related_name='exchanges_from')
    to_currency         = models.ForeignKey(Currency, on_delete=models.CASCADE,related_name='exchanges_to')
    
    def clean(self):
        if self.from_currency == self.to_currency:
            raise ValidationError("From and To currencies must be different.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def getYahooExchSymbol(self):
        return urllib.parse.quote(f"{self.from_currency.code}{self.to_currency.code}=X")
    
    def __str__(self):
        return f"{self.from_currency.code} - {self.to_currency.code}"

class ExchangeRates(BaseModelMixin):
    currency_exchange   = models.ForeignKey(CurrencyExchange, on_delete=models.CASCADE, related_name='currencyExch')
    date                = models.DateField()
    open_rate           = models.DecimalField(max_digits=10, decimal_places=4)
    high_rate           = models.DecimalField(max_digits=10, decimal_places=4)
    low_rate            = models.DecimalField(max_digits=10, decimal_places=4)
    close_rate          = models.DecimalField(max_digits=10, decimal_places=4)
    adj_close_rate      = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        db_table ='exchange-rates'
        unique_together = ('currency_exchange', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.currency_exchange.from_currency.code}/{self.currency_exchange.to_currency.code} on {self.date}"

    