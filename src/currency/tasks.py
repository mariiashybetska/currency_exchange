from celery import shared_task

from currency.parse_functions import _pb, _mono, _vkurse


@shared_task
def parse_rates():
    _pb()
    _mono()
    _vkurse()





