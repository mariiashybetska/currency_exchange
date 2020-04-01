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
    path('experience/', TemplateView.as_view(template_name='experience.html'),name='experience'),
    path('education/', TemplateView.as_view(template_name='education.html'), name='education'),
    path('skills/', TemplateView.as_view(template_name='skills.html'),name='skills'),
    path('interests/', TemplateView.as_view(template_name='interests.html'), name='interests'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
