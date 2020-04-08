from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('account/', include('account.urls')),
    path('currency/', include('currency.urls')),

    # API
    path('api/v1/currency/', include('currency.api.urls')),
    path('api/v1/account/', include('account.api.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # CV
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('experience/', TemplateView.as_view(template_name='experience.html'),name='experience'),
    path('education/', TemplateView.as_view(template_name='education.html'), name='education'),
    path('skills/', TemplateView.as_view(template_name='skills.html'),name='skills'),
    path('interests/', TemplateView.as_view(template_name='interests.html'), name='interests'),

]

# SWAGGER
schema_view = get_swagger_view(title='DOCS')
urlpatterns.append(path('api/v1/docs/', schema_view))


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
