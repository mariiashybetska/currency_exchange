import requests

from currency.models import Rate
from currency import model_choices as mch

from decimal import Decimal


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
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(r_json[rate]['buy'][:5]),
                'sale': Decimal(r_json[rate]['sale'][:5]),
                'source': mch.SRC_VK,
            }



            new_rate = Rate(**rate_kwargs)
            last_rate = Rate.objects.filter(currency=currency, source=mch.SRC_VK).last()

            if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                new_rate.save()



def _mtb(*args, **kwargs):
    import requests
    from bs4 import BeautifulSoup

    url = 'https://mtb.ua/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    usd_dictionary = dict()
    eur_dictionary = dict()
    class_buy_sell_dict = {'exchange-value tab-item active': 'Покупка',
                           'exchange-value tab-item': 'Продажа'}

    for class_name, buy_or_sell in class_buy_sell_dict.items():
        buy_sell_curr = list(soup.findAll('div', attrs={'class': class_name}))[0]
        # exchange-value_currency - name of currency
        currencies = list(buy_sell_curr.findAll('div', attrs={'class': 'exchange-value_currency'}))

        # Finding index with necessary currency
        for i in range(len(currencies)):
            curr = list(currencies)[i]
            act_curr = curr.get_text().split()[0]

            # exchange-value_num - exchange rate
            if act_curr in ['USD', 'EUR']:
                usd_index = i
                usd_dictionary[buy_or_sell] = float(
                    list(buy_sell_curr.findAll('span', attrs={'class': 'exchange-value_num'}))[
                        usd_index].get_text().split()[0])

            elif act_curr == 'EUR':
                eur_index = i
                eur_dictionary[buy_or_sell] = float(
                    list(buy_sell_curr.findAll('span', attrs={'class': 'exchange-value_num'}))[
                        eur_index].get_text().split()[0])
