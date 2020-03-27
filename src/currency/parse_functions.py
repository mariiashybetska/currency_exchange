import requests

from currency.models import Rate
from currency import model_choices as mch

from decimal import Decimal
from bs4 import BeautifulSoup


def _pb():
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
            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SRC_PB).last()

            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()


def _mono():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    r_json = response.json()

    for rate in r_json:
        if rate['currencyCodeA']:
            if rate['currencyCodeA'] in {840, 978} and rate['currencyCodeB'] == 980:
                # print(rate['currencyCodeA'], rate['rateSell'], rate['rateBuy'])

                currency = {
                    840: mch.CURR_USD,
                    978: mch.CURR_EUR,
                }[rate['currencyCodeA']]

                rate_kwargs = {
                    'currency': currency,
                    'buy': round(Decimal(rate['rateBuy']), 2),
                    'sale': round(Decimal(rate['rateSell']), 2),
                    'source': mch.SRC_MB,
                }

                # Rate.objects.create(**rate_kwargs)
                new_rate = Rate(**rate_kwargs)
                last_rate = Rate.objects.filter(currency=currency, source=mch.SRC_MB).last()

                if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                    new_rate.save()


def _vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    r_json = response.json()

    for rate in r_json:
        if rate in {'Dollar', 'Euro'}:
            currency = {
                'Dollar': mch.CURR_USD,
                'Euro': mch.CURR_EUR
            }[rate]
            buy = r_json[rate]['buy'][:5].replace(',', '.')
            sale = r_json[rate]['sale'][:5].replace(',', '.')
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(buy),
                'sale': Decimal(sale),
                'source': mch.SRC_VK,
            }

            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SRC_VK).last()

            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()



