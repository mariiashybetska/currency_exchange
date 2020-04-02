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


def _mtb():
    url = 'https://mtb.ua/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    rates = soup.find_all('div', attrs={"class": "exchange-value_item"})

    currencies = {
        'USD': [],
        'EUR': [],
    }

    for rate in rates:
        c = rate.find_all('div', attrs={"class": "exchange-value_currency"})[0].contents[0].strip()
        if c in {'USD', 'EUR'}:
            c_rate = rate.find_all('span', attrs={"class": "exchange-value_num"})[0].contents[0].strip()
            currencies[c].append(c_rate)

    for key, value in currencies.items():
        currency = {
            'USD': mch.CURR_USD,
            'EUR': mch.CURR_EUR,
        }[key]
        rate_kwargs = {
            'currency': currency,
            'sale': Decimal(value[0]),
            'buy': Decimal(value[1]),
            'source': mch.SRC_MTB,
        }
        new_rate = Rate(**rate_kwargs)
        last_rate = Rate.objects.filter(currency=currency, source=mch.SRC_MTB).last()

        if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
            new_rate.save()


def _alpha():
    url = 'https://alfabank.ua/currency-exchange'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')
    html = list(soup.children)[6]
    body = list(html.children)[3]
    currencies = list(body.find_all('div', attrs={'class': 'exchange-data-currency'}))

    for curr in currencies:
        if curr.get_text() == 'USD/UAH':
            sale = list(body.find_all('span', attrs={'class': 'rate-number', 'data-currency': 'USD_SALE'}))[0]
            buy = list(body.find_all('span', attrs={'class': 'rate-number', 'data-currency': 'USD_BUY'}))[0]
            rate_kwargs = {
                'currency': mch.CURR_USD,
                'sale': Decimal(sale.get_text().strip()),
                'buy': Decimal(buy.get_text().strip()),
                'source': mch.SRC_ALPHA,
            }
        elif curr.get_text() == 'EUR/UAH':
            sale = list(body.find_all('span', attrs={'class': 'rate-number', 'data-currency': 'EUR_SALE'}))[0]
            buy = list(body.find_all('span', attrs={'class': 'rate-number', 'data-currency': 'EUR_BUY'}))[0]
            rate_kwargs = {
                'currency': mch.CURR_EUR,
                'sale': Decimal(sale.get_text().strip()),
                'buy': Decimal(buy.get_text().strip()),
                'source': mch.SRC_ALPHA,
            }
        else:
            continue

        new_rate = Rate(**rate_kwargs)
        last_rate = Rate.objects.filter(currency=new_rate.currency, source=mch.SRC_ALPHA).last()

        if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
            new_rate.save()


def _concord():
    url = 'https://concord.ua/'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')
    html = list(soup.children)[2]
    body = list(html.children)[3]
    rates = body.find_all('p', attrs={'class': 'news-block__course-block'})

    for rate in rates:
        c = list(rate.find_all('span', attrs={'class': 'news-block__course-type'}))[0].get_text().strip()
        currency = {
            'Долар': mch.CURR_USD,
            'Євро': mch.CURR_EUR,
        }.get(c)

        if currency:
            c_rate = list(rate.find_all('span', attrs={'class': 'news-block__course-data'}))[
                0].get_text().strip().split('/')

            if len(c_rate) == 2:
                rate_kwargs = {
                    'currency': currency,
                    'sale': Decimal(c_rate[1].strip()),
                    'buy': Decimal(c_rate[0].strip()),
                    'source': mch.SRC_CONCORD,
                }

                new_rate = Rate(**rate_kwargs)
                last_rate = Rate.objects.filter(currency=currency, source=mch.SRC_CONCORD).last()

                if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
                    new_rate.save()

