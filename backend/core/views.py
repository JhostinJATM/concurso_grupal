"""
Views base para la API REST.
Implementa principios SOLID y patrones de diseño.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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


class CustomAuthToken(ObtainAuthToken):
    """
    Vista personalizada para autenticación por token.
    Extiende ObtainAuthToken para retornar información adicional del usuario.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.pk,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })


class LogoutView(APIView):
    """
    Vista para cerrar sesión y eliminar el token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Eliminar el token del usuario actual
            request.user.auth_token.delete()
            return Response({'detail': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Error al cerrar sesión'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Vista para obtener la información del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
        })


class RegisterView(APIView):
    """
    Vista para registrar nuevos usuarios.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        # Validaciones básicas
        if not username or not password:
            return Response(
                {'detail': 'Usuario y contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'detail': 'El nombre de usuario ya existe'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            
            # Crear el token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.pk,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'detail': 'Error al crear el usuario'},
                status=status.HTTP_400_BAD_REQUEST
            )
