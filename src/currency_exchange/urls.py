from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('account/', include('account.urls')),
    path('currency/', include('currency.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
