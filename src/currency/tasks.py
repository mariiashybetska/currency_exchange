from celery import shared_task

from currency.parse_functions import _pb, _mono


@shared_task
def parse_rates(self):
    _pb()
    _mono()




