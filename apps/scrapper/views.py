from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
# Create your views here.
from .service import run_scraper
from .models import Currency,CurrencyExchange,ExchangeRates
from .serializers import ExchangeRatesSerializer


DURATION_MAPPING = {
                '1W': timedelta(weeks=1),
                '1M': timedelta(weeks=4),
                '3M': timedelta(weeks=12),
                '6M': timedelta(weeks=26),
                '1Y': timedelta(weeks=52)
            }

class TriggerScrapper(APIView):
    def get(self,request):
        try:
            run_scraper()
            return Response(data={
                'success':True,
                'message':'Scrapping Succesful'
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success':False,
                                'message':'Something went wrong on our side',
                                'data':{}},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExchangeRatesView(APIView):
    def get(self,request):
        try:
            from_curr = request.query_params.get('from')
            to_curr   = request.query_params.get('to')
            period    = request.query_params.get('period')
            
            if from_curr!=to_curr and from_curr in Currency.CURRENCY_CHOICES and to_curr in Currency.CURRENCY_CHOICES and period in DURATION_MAPPING:
                from_curr_inst = Currency.objects.get(code=from_curr)
                to_curr_inst   = Currency.objects.get(code=to_curr)
                curr_pair_inst = CurrencyExchange.objects.get(from_currency=from_curr_inst,to_currency=to_curr_inst)
                now            = timezone.now()
                start_date     = now - DURATION_MAPPING[period]
                
                queryset = ExchangeRates.objects.filter(
                            currency_exchange=curr_pair_inst,
                            date__gte=start_date
                            ).order_by('-date')
                serializer = ExchangeRatesSerializer(queryset, many=True)
                return Response(data={
                    'success':True,
                    'message':"Data fetched successfully",
                    'data':serializer.data
                },status=status.HTTP_200_OK)
            else:
                return Response(data={
                    'success':False,
                    'message':"Invalid data format, refer the guide",
                    'data':{
                        "from":Currency.CURRENCY_CHOICES,
                        "to":Currency.CURRENCY_CHOICES,
                        "period":[k for k in DURATION_MAPPING],
                        "note":"from and to currencies need to be different"
                        }
                },status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(data={'success':False,
                                  'message':'Something went wrong on our side',
                                  'data':{}},status=status.HTTP_500_INTERNAL_SERVER_ERROR)