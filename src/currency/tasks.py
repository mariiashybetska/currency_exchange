from celery import shared_task

from currency.parse_functions import _pb, _mono, _vkurse, _mtb, _alpha, _concord


@shared_task
def parse_rates():
    _pb()
    _mono()
    _vkurse()
    _mtb()
    _alpha()
    _concord()




