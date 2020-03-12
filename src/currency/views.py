from django.shortcuts import render
from django.views.generic.list import ListView

from currency.models import Rate


class RateListView(ListView):
    model = Rate
    template_name = 'rates.html'
    paginate_by = 20
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

