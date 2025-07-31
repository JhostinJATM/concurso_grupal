"""
URLs para la aplicación de Cajones Inteligentes.
Configuración de todas las rutas de la API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CajonViewSet,
    ObjetoViewSet,
    HistorialViewSet,
    RecomendacionViewSet,
    EstadisticasViewSet,
    ConfiguracionViewSet,
    CajonManagementViewSet
)

app_name = 'cajones_inteligentes'

# Router para ViewSets
router = DefaultRouter()
router.register(r'cajones', CajonViewSet, basename='cajon')
router.register(r'objetos', ObjetoViewSet, basename='objeto')
router.register(r'historial', HistorialViewSet, basename='historial')
router.register(r'recomendaciones', RecomendacionViewSet, basename='recomendacion')
router.register(r'estadisticas', EstadisticasViewSet, basename='estadisticas')
router.register(r'configuracion', ConfiguracionViewSet, basename='configuracion')
router.register(r'gestion-cajones', CajonManagementViewSet, basename='gestion-cajones')

urlpatterns = [
    # Incluir todas las rutas del router
    path('', include(router.urls)),
]

