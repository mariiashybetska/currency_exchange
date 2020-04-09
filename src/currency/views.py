from django.views.generic import TemplateView
from django.views.generic.list import ListView, View
from django.http import HttpResponse
from django_filters.views import FilterView
from django.core.cache import cache

from urllib.parse import urlencode
import csv

from currency.models import Rate
from currency.filters import RateFilter
from currency import model_choices as mch
from currency.utils import geterate_rate_cache_key


class RateListView(FilterView):
    filterset_class = RateFilter
    model = Rate
    template_name = 'rates.html'
    paginate_by = 10
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = dict(self.request.GET.items())

        if 'page' in query_params:
            del query_params['page']

        context['query_params'] = urlencode(query_params)

        return context


class LatestRates(TemplateView):
    template_name = 'latestrates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rates = []

        for bank in mch.SOURCE_CHOICES:
            source = bank[0]
            # rates[bank[0]] = {'display': bank[1]}
            for curr in mch.CURRENCY_CHOICES:
                currency = curr[0]
                cache_key = geterate_rate_cache_key(source, currency)

                rate = cache.get(cache_key)
                if rate is None:
                    rate = Rate.objects.filter(source=source, currency=currency).order_by('created').last()
                    if rate:
                        rate_dict = {
                            'currency': rate.get_currency_display,
                            'source': rate.get_source_display,
                            'buy': rate.buy,
                            'sale': rate.sale,
                            'created': rate.created,
                        }
                        rates.append(rate_dict)
                        cache.set(cache_key, rate_dict, 5) # 15 minutes
                else:
                    rates.append(rate)


        context['rates'] = rates
        # Rate.objects.filter(source=mch.SRC_PB, currency=mch.CURR_USD).order_by('created').last()
        return context



'''
created = models.DateTimeField(auto_now_add=True)
currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
sale = models.DecimalField(max_digits=4, decimal_places=2)
buy = models.DecimalField(max_digits=4, decimal_places=2)
source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
'''


class RateCSV(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rates.csv"'
        writer = csv.writer(response)
        headers = [
            'id',
            'created',
            'currency',
            'sale',
            'buy',
            'source',
        ]
        writer.writerow(headers)
        for rate in Rate.objects.all().iterator():
            writer.writerow(map(str, [
                rate.id,
                rate.created,
                rate.get_currency_display(),
                rate.sale,
                rate.buy,
                rate.get_source_display(),
            ]))
        return response
