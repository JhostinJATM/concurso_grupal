"""
Views base para la API REST.
Implementa principios SOLID y patrones de diseño.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from .serializers import DetailSerializer


class HealthCheckView(APIView):
    """
    Vista para verificar el estado de la API.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Endpoint de health check.
        """
        return Response({
            'status': 'healthy',
            'message': 'Smart Drawers Backend API is running',
            'version': '1.0.0'
        }, status=status.HTTP_200_OK)


class BaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet base que implementa funcionalidades comunes.
    Sigue principios SOLID, especialmente Single Responsibility.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar por registros activos por defecto.
        Puede ser overrideado por subclases.
        """
        queryset = super().get_queryset()
        if hasattr(self.queryset.model, 'is_active'):
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        """
        Override para agregar usuario actual al contexto.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Override para agregar usuario actual al contexto.
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        """
        Eliminación lógica del objeto.
        """
        instance = self.get_object()
        
        if hasattr(instance, 'soft_delete'):
            with transaction.atomic():
                instance.soft_delete()
            
            serializer = DetailSerializer(data={'detail': 'Registro eliminado correctamente'})
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {'detail': 'Eliminación lógica no soportada para este modelo'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """
        Restaurar un objeto eliminado lógicamente.
        """
        # Para restore, necesitamos obtener todos los objetos, incluso inactivos
        queryset = self.queryset.model.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        
        if hasattr(instance, 'restore'):
            with transaction.atomic():
                instance.restore()
            
            serializer = DetailSerializer(data={'detail': 'Registro restaurado correctamente'})
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {'detail': 'Restauración no soportada para este modelo'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ReadOnlyBaseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet base para operaciones de solo lectura.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar por registros activos por defecto.
        """
        queryset = super().get_queryset()
        if hasattr(self.queryset.model, 'is_active'):
            queryset = queryset.filter(is_active=True)
        return queryset
