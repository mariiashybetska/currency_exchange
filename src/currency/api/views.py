from rest_framework import generics as g
from django_filters import rest_framework as f

from currency.api.serializers import RateSerializer
from currency.models import Rate


class RateFilter(f.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'created': ['exact', 'gt', 'lt', 'gte', 'lte', ],
            'currency': ['exact', ],
            'source': ['exact', ],
        }


class RatesView(g.ListCreateAPIView):
    # GET, POST
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (f.DjangoFilterBackend,)
    filterset_class = RateFilter


class RateView(g.RetrieveUpdateDestroyAPIView):
    # GET, PUT, PATCH, DELETE
    queryset = Rate.objects.all()
    serializer_class = RateSerializer