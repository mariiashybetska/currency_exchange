from rest_framework import generics

from currency.api.serializers import RateSerializer
from currency.models import Rate


class RatesView(generics.ListCreateAPIView):
    # GET, POST
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateView(generics.RetrieveUpdateDestroyAPIView):
    # GET, PUT, PATCH, DELETE
    queryset = Rate.objects.all()
    serializer_class = RateSerializer