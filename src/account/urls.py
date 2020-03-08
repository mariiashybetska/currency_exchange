from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('smoke/', views.smoke, name='smoke'),
    path('profile/<int:pk>/', views.MyProfile.as_view(), name='my-profile'),
    path('contact-us/', views.ContactUS.as_view(), name='contact'),

]
