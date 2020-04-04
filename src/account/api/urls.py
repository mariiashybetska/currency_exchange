from django.urls import path

from account.api import views

app_name = 'api-account'

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('contacts/<int:pk>/', views.ContactView.as_view(), name='contact'),
]