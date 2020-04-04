import pytest
import requests
from decimal import Decimal

from django.urls import reverse

from currency.tasks import _pb, _mono
from currency.models import Rate


def test_sanity():
    assert 200 == 200


def test_index_page(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


def test_rates_not_auth(client):
    url = reverse('api-currency:rates')
    response = client.get(url)
    assert response.status_code == 401
    resp_j = response.json()
    assert len(resp_j) == 1
    assert resp_j['detail'] == 'Authentication credentials were not provided.'


def test_rates_auth(api_client, user):
    url = reverse('api-currency:rates')
    response = api_client.get(url)
    assert response.status_code == 401

    api_client.login(user.username, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


def test_get_rates(api_client, user):
    url = reverse('api-currency:rates')
    api_client.login(user.email, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


def test_send_email():
    from django.core import mail
    from account.tasks import send_activation_code_async
    from uuid import uuid4

    emails = mail.outbox
    print('EMAILS:', emails)

    send_activation_code_async.delay(1, str(uuid4()))
    emails = mail.outbox
    assert len(emails) == 1

    email = mail.outbox[0]
    assert email.subject == 'Your activation code'


# homework

class Response:
    pass


def test_task_pb(mocker):

    def mock():
        response = Response()
        response.json = lambda: [
            {"ccy": "USD", "base_ccy": "UAH", "buy": "27.10", "sale": "27.65"},
            {"ccy": "EUR", "base_ccy": "UAH", "buy": "29.20", "sale": "29.86"},
            {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.34", "sale": "0.36"},
            {"ccy": "BTC", "base_ccy": "USD", "buy": "6464.6154", "sale": "7145.1012"},
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    Rate.objects.all().delete()

    _pb()
    rate = Rate.objects.all()
    assert len(rate) == 2
    assert rate[0].currency == 1
    assert rate[0].buy == Decimal('27.20')
    assert rate[0].sale == Decimal('27.62')
    assert rate[0].source == 1
    assert rate[1].currency == 2
    assert rate[1].buy == Decimal('29.30')
    assert rate[1].sale == Decimal('29.85')
    assert rate[1].source == 1

    Rate.objects.all().delete()


def test_task_mono(mocker):

    def mock():
        response = Response()
        response.json = lambda: [
            {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1585948209, "rateBuy": 27.35, "rateSell": 27.62},
            {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1585948209, "rateBuy": 29.45, "rateSell": 29.83},
            {"currencyCodeA": 643, "currencyCodeB": 980, "date": 1585948209, "rateBuy": 0.315, "rateSell": 0.36},
            {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1585948209, "rateBuy": 1.0863, "rateSell": 1.11},
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _mono()
    rate = Rate.objects.all()
    assert len(rate) == 2
    assert rate[0].currency == 1
    assert rate[0].buy == Decimal('27.35')
    assert rate[0].sale == Decimal('27.62')
    assert rate[0].source == 2
    assert rate[1].currency == 2
    assert rate[1].buy == Decimal('29.45')
    assert rate[1].sale == Decimal('29.83')
    assert rate[1].source == 2
    Rate.objects.all().delete()