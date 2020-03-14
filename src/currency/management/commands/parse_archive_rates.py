from django.core.management.base import BaseCommand

import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from currency.models import Rate
from currency import model_choices as mch


class Command(BaseCommand):
    help = 'Parse archive rates from PrivataBank at this day 4 years ago'

    def handle(self, *args, **options):
        url = 'https://api.privatbank.ua/p24api/exchange_rates'
        d = (date.today() + relativedelta(years=-4)).strftime("%d.%m.%Y")
        api_params = {
            'json': '',
            'date': d,
        }

        r = requests.get(url, params=api_params)
        r_json = r.json()

        for rate in r_json['exchangeRate']:
            if 'currency' in rate:
                if rate['currency'] in {'EUR', 'USD'}:
                    currency = {
                        'EUR': mch.CURR_EUR,
                        'USD': mch.CURR_USD,
                    }[rate['currency']]

                    if 'purchaseRate' and 'saleRate' in rate:
                        rate_kwargs = {
                            'currency': currency,
                            'buy': round(Decimal(rate['saleRate']), 2),
                            'sale': round(Decimal(rate['purchaseRate']), 2),
                            'source': mch.SRC_PB,
                        }
                    else:
                        rate_kwargs = {
                            'currency': currency,
                            'buy': round(Decimal(rate['saleRateNB']), 2),
                            'sale': round(Decimal(rate['purchaseRateNB']), 2),
                            'source': mch.SRC_PB,
                        }
                    Rate(**rate_kwargs).save()
                    r = Rate.objects.filter(currency=currency, source=mch.SRC_PB).last()
                    r.created = datetime.now() + relativedelta(years=-4)
                    r.save()
