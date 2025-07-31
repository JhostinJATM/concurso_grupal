"""
URL configuration for Smart Drawers Backend.
Configuración principal de URLs siguiendo principios de arquitectura limpia.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

# Router principal para API REST
api_router = DefaultRouter()

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API REST
    path('api/v1/', include(api_router.urls)),
    path('api/v1/', include('cajones_inteligentes.urls')),
    path('api/v1/', include('core.urls')),
    
    # Autenticación DRF
    path('api-auth/', include('rest_framework.urls')),
    
    # Documentación de la API con drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Servir archivos media y static en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
