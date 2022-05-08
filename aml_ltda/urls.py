from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('apps.authentication.urls')),
    path('', include('apps.home.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('service/', include('apps.service.urls')),
    path('system/', include('apps.system.urls')),
    path('mural/', include('apps.mural.urls')),
    path('finance/', include('apps.finance.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
