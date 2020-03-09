import requests
from bs4 import BeautifulSoup
from decimal import Decimal


url = 'https://alfabank.ua/currency-exchange'
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')
html = list(soup.children)[6]
body = list(html.children)[3]
#print(body)
rates = list(body.find_all('span', attrs={'class': 'rate-number'}))
print(rates)
USD_buy = list(body.find_all('span', attrs={'class': 'rate-number', 'data-currency': 'USD_BUY'}))[0].get_text().strip()
USD_sale = list(body.find_all('span', attrs={'class': 'rate-number', 'data-currency': 'USD_SALE'}))[0].get_text().strip()
EUR_buy = list(body.find_all('span', attrs={'class': 'rate-number', 'data-currency': 'EUR_BUY'}))[0].get_text().strip()
EUR_sale = list(body.find_all('span', attrs={'class': 'rate-number', 'data-currency': 'EUR_SALE'}))[0].get_text().strip()
print(f'USD buy: {USD_buy} USD sale: {USD_sale}')
print(f'EUR buy: {EUR_buy} EUR sale: {EUR_sale}')

url2 = 'http://vkurse.dp.ua/'
r2 = requests.get(url2)

soup2 = BeautifulSoup(r2.content, 'html.parser')
soup2.find_all('div', attrs={})