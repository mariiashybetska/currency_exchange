from celery import shared_task
import requests

from currency.models import Rate
from currency import model_choices as mch

from decimal import Decimal


def _pb(self):
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    r_json = response.json()
    for rate in r_json:
        if rate['ccy'] in {'USD', 'EUR'}:
            # print(rate['ccy'], rate['buy'], rate['sale'])
            # currency = mch.CURR_USD if rate['ccy'] == 'USD' else mch.CURR_EUR
            currency = {
                'USD': mch.CURR_USD,
                'EUR': mch.CURR_EUR,
            }[rate['ccy']]

            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['buy']),
                'sale': Decimal(rate['sale']),
                'source': mch.SRC_PB,
            }

            # Rate.objects.create(**rate_kwargs)
            new_rate = Rate.objects.create(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SRC_PB).last()

            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()


# def _mono(self):
#     url = 'https://api.monobank.ua/bank/currency'
#     response = requests.get(url)
#     r_json = response.json()
#
#     for rate in r_json:
#         if rate['currencyCodeA'] in {840, 978} and rate['currencyCodeB'] == 980:
#             print(rate['currencyCodeA'], rate['rateSell'], rate['rateBuy'])
#
#             currency = {
#                 '840': mch.CURR_USD,
#                 '978': mch.CURR_EUR,
#             }[rate['currencyCodeA']]
#
#             rate_kwargs = {
#                 'currency': currency,
#                 'buy': Decimal(rate['rateBuy']),
#                 'sale': Decimal(rate['rateSell']),
#                 'source': mch.SRC_MB,
#             }
#
#             # Rate.objects.create(**rate_kwargs)
#             new_rate = Rate.objects.create(**rate_kwargs)
#             last_rate = Rate.objects.filter(currency=currency, source=mch.SRC_MB).last()
#
#             if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
#                 new_rate.save()

@shared_task
def parse_rate(self):
    _pb()
    # _mono()




