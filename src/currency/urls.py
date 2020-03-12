from django.urls import path

from currency import views

app_name = 'currency'

urlpatterns = [
    path('latest-rates/', views.RateListView.as_view(), name='rates'),
    path('download/rates', views.RateCSV.as_view(), name='download-rates')
]


