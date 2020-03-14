from django.views.generic.list import ListView, View
from django.http import HttpResponse

import csv

from currency.models import Rate


class RateListView(ListView):
    model = Rate
    template_name = 'rates.html'
    paginate_by = 20
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
