import django_filters as f
from django.forms import DateInput

from currency.models import Rate


class RateFilter(f.FilterSet):
    created_date = f.DateFilter(field_name='created',
                                lookup_expr='date',
                                widget=DateInput(
                                    attrs={
                                        'class': 'datepicker',
                                        'type': 'date',
                                    }
                                ))

    class Meta:
        model = Rate
        fields = ['sale', 'source', 'created_date',]