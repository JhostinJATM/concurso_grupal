"""
Views para la aplicación de Cajones Inteligentes.
Implementa principios SOLID y Clean Architecture.
"""
import logging
from datetime import timedelta
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from django.db.models import Count, Q, F
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.views import BaseViewSet, ReadOnlyBaseViewSet
from core.serializers import DetailSerializer
from .models import Cajon, Objeto, Historial, Recomendacion, TipoObjeto, Tamanio
from .serializers import (
    CajonSerializer, CajonListSerializer,
    ObjetoSerializer, ObjetoListSerializer,
    HistorialSerializer, RecomendacionSerializer,
    EstadisticasSerializer, TipoObjetoSerializer, TamanioSerializer
)
from .services import RecomendacionService

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Listar cajones",
        description="Obtiene una lista paginada de todos los cajones del usuario autenticado.",
        tags=["Cajones"]
    ),
    create=extend_schema(
        summary="Crear cajón",
        description="Crea un nuevo cajón para el usuario autenticado.",
        tags=["Cajones"]
    ),
    retrieve=extend_schema(
        summary="Obtener cajón",
        description="Obtiene los detalles de un cajón específico.",
        tags=["Cajones"]
    ),
    update=extend_schema(
        summary="Actualizar cajón",
        description="Actualiza completamente un cajón existente.",
        tags=["Cajones"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente cajón",
        description="Actualiza parcialmente un cajón existente.",
        tags=["Cajones"]
    ),
    destroy=extend_schema(
        summary="Eliminar cajón",
        description="Elimina lógicamente un cajón (los objetos se quedan sin cajón asignado).",
        tags=["Cajones"]
    )
)
class CajonViewSet(BaseViewSet):
    """
    ViewSet para gestionar cajones.
    Implementa CRUD completo con funcionalidades adicionales.
    """
    serializer_class = CajonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['capacidad_maxima']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'capacidad_maxima', 'created_at']
    ordering = ['nombre']

    def get_queryset(self):
        """Filtrar cajones por usuario autenticado."""
        return Cajon.objects.filter(
            usuario=self.request.user,
            is_active=True
        ).select_related('usuario').prefetch_related('objetos')

    def get_serializer_class(self):
        """Usar serializador simplificado para list."""
        if self.action == 'list':
            return CajonListSerializer
        return CajonSerializer

    def perform_create(self, serializer):
        """Asignar usuario actual al crear cajón."""
        cajon = serializer.save(usuario=self.request.user)
        
        # Crear entrada en historial
        Historial.objects.create(
            nombre=f"Cajón creado: {cajon.nombre}",
            motivo=f"Se creó un nuevo cajón con capacidad para {cajon.capacidad_maxima} objetos",
            usuario=self.request.user,
            cajon=cajon,
            tipo_accion='CREAR'
        )

    def perform_update(self, serializer):
        """Registrar actualización en historial."""
        instance = serializer.instance
        old_name = instance.nombre
        
        cajon = serializer.save()
        
        # Crear entrada en historial
        Historial.objects.create(
            nombre=f"Cajón modificado: {old_name} -> {cajon.nombre}",
            motivo=f"Se modificó el cajón. Nueva capacidad: {cajon.capacidad_maxima}",
            usuario=self.request.user,
            cajon=cajon,
            tipo_accion='MODIFICAR'
        )

    @action(detail=True, methods=['get'])
    def objetos(self, request, pk=None):
        """Obtener todos los objetos de un cajón específico."""
        cajon = self.get_object()
        objetos = cajon.objetos.filter(is_active=True)
        
        # Aplicar filtros opcionales
        tipo_objeto = request.query_params.get('tipo_objeto')
        tamanio = request.query_params.get('tamanio')
        
        if tipo_objeto:
            objetos = objetos.filter(tipo_objeto=tipo_objeto)
        if tamanio:
            objetos = objetos.filter(tamanio=tamanio)
        
        serializer = ObjetoListSerializer(objetos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtener estadísticas específicas de un cajón."""
        cajon = self.get_object()
        objetos = cajon.objetos.filter(is_active=True)
        
        stats = {
            'nombre_cajon': cajon.nombre,
            'capacidad_maxima': cajon.capacidad_maxima,
            'objetos_actuales': objetos.count(),
            'capacidad_disponible': cajon.capacidad_disponible,
            'porcentaje_ocupacion': (objetos.count() / cajon.capacidad_maxima) * 100,
            'objetos_por_tipo': dict(
                objetos.values('tipo_objeto').annotate(
                    count=Count('id')
                ).values_list('tipo_objeto', 'count')
            ),
            'objetos_por_tamanio': dict(
                objetos.values('tamanio').annotate(
                    count=Count('id')
                ).values_list('tamanio', 'count')
            ),
            'esta_lleno': cajon.esta_lleno
        }
        
        return Response(stats)


class ObjetoViewSet(BaseViewSet):
    """
    ViewSet para gestionar objetos.
    Implementa los métodos de negocio requeridos.
    """
    serializer_class = ObjetoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_objeto', 'tamanio', 'cajon']
    search_fields = ['nombre', 'descripcion', 'codigo']
    ordering_fields = ['nombre', 'fecha_ingreso', 'tipo_objeto']
    ordering = ['-fecha_ingreso']

    def get_queryset(self):
        """Filtrar objetos por cajones del usuario autenticado."""
        return Objeto.objects.filter(
            cajon__usuario=self.request.user,
            is_active=True
        ).select_related('cajon', 'cajon__usuario')

    def get_serializer_class(self):
        """Usar serializador simplificado para list."""
        if self.action == 'list':
            return ObjetoListSerializer
        return ObjetoSerializer

    def perform_create(self, serializer):
        """Crear objeto y registrar en historial."""
        with transaction.atomic():
            objeto = serializer.save()
            
            # Crear entrada en historial
            Historial.objects.create(
                nombre=f"Objeto creado: {objeto.nombre}",
                motivo=f"Se agregó el objeto '{objeto.nombre}' al cajón '{objeto.cajon.nombre if objeto.cajon else 'Sin asignar'}'",
                usuario=self.request.user,
                objeto=objeto,
                cajon=objeto.cajon,
                tipo_accion='CREAR'
            )

    def perform_update(self, serializer):
        """Actualizar objeto y registrar en historial."""
        instance = serializer.instance
        old_name = instance.nombre
        old_cajon = instance.cajon
        
        with transaction.atomic():
            objeto = serializer.save()
            
            # Determinar tipo de cambio
            if old_cajon != objeto.cajon:
                motivo = f"Se movió el objeto '{old_name}' de '{old_cajon.nombre if old_cajon else 'Sin asignar'}' a '{objeto.cajon.nombre if objeto.cajon else 'Sin asignar'}'"
                tipo_accion = 'MOVER'
            else:
                motivo = f"Se modificó el objeto '{old_name}' -> '{objeto.nombre}'"
                tipo_accion = 'MODIFICAR'
            
            # Crear entrada en historial
            Historial.objects.create(
                nombre=f"Objeto {tipo_accion.lower()}: {objeto.nombre}",
                motivo=motivo,
                usuario=self.request.user,
                objeto=objeto,
                cajon=objeto.cajon,
                tipo_accion=tipo_accion
            )

    @action(detail=False, methods=['post'])
    def nuevo_objeto(self, request):
        """
        Endpoint para crear objeto usando el método nuevo_objeto.
        Implementa el método nuevoObjeto requerido.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            objeto = Objeto.nuevo_objeto(**serializer.validated_data)
            
            # Crear entrada en historial
            Historial.objects.create(
                nombre=f"Objeto creado (método nuevo_objeto): {objeto.nombre}",
                motivo=f"Se creó el objeto '{objeto.nombre}' usando el método nuevo_objeto",
                usuario=request.user,
                objeto=objeto,
                cajon=objeto.cajon,
                tipo_accion='CREAR'
            )
        
        response_serializer = ObjetoSerializer(objeto)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def modificar_objeto(self, request, pk=None):
        """
        Endpoint para modificar objeto usando el método modificar_objeto.
        Implementa el método modificarObjeto requerido.
        """
        objeto = self.get_object()
        nombre = request.data.get('nombre')
        info = {k: v for k, v in request.data.items() if k != 'nombre'}
        
        with transaction.atomic():
            objeto_modificado = objeto.modificar_objeto(nombre=nombre, **info)
            
            # Crear entrada en historial
            Historial.objects.create(
                nombre=f"Objeto modificado (método modificar_objeto): {objeto_modificado.nombre}",
                motivo=f"Se modificó el objeto usando el método modificar_objeto",
                usuario=request.user,
                objeto=objeto_modificado,
                cajon=objeto_modificado.cajon,
                tipo_accion='MODIFICAR'
            )
        
        serializer = ObjetoSerializer(objeto_modificado)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def eliminar_objeto(self, request, pk=None):
        """
        Endpoint para eliminar objeto usando el método eliminar_objeto.
        Implementa el método eliminarObjeto requerido.
        """
        objeto = self.get_object()
        nombre_objeto = objeto.nombre
        cajon_nombre = objeto.cajon.nombre
        
        with transaction.atomic():
            objeto.eliminar_objeto()
            
            # Crear entrada en historial
            Historial.objects.create(
                nombre=f"Objeto eliminado: {nombre_objeto}",
                motivo=f"Se eliminó el objeto '{nombre_objeto}' del cajón '{cajon_nombre}'",
                usuario=request.user,
                cajon_id=objeto.cajon.id,
                tipo_accion='ELIMINAR'
            )
        
        return Response(
            {'detail': f'Objeto "{nombre_objeto}" eliminado correctamente'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def consultar_objeto(self, request):
        """
        Endpoint para consultar objetos usando el método consultar_objeto.
        Implementa el método consultarObjeto requerido.
        """
        nombre = request.query_params.get('nombre')
        codigo = request.query_params.get('codigo')
        
        if not nombre and not codigo:
            return Response(
                {'detail': 'Debe proporcionar al menos nombre o código'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        objetos = Objeto.consultar_objeto(nombre=nombre, codigo=codigo)
        # Filtrar por usuario
        objetos = objetos.filter(cajon__usuario=request.user)
        
        serializer = ObjetoListSerializer(objetos, many=True)
        
        # Registrar consulta en historial
        Historial.objects.create(
            nombre=f"Consulta de objetos",
            motivo=f"Búsqueda por nombre: '{nombre}', código: '{codigo}'",
            usuario=request.user,
            tipo_accion='CONSULTAR'
        )
        
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def ordenar_por_tipo(self, request):
        """
        Endpoint para obtener objetos ordenados por tipo.
        Implementa el método ordenarTipo requerido.
        """
        objetos = Objeto.ordenar_por_tipo().filter(cajon__usuario=request.user)
        serializer = ObjetoListSerializer(objetos, many=True)
        return Response(serializer.data)


class HistorialViewSet(ReadOnlyBaseViewSet):
    """
    ViewSet de solo lectura para el historial.
    """
    serializer_class = HistorialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_accion', 'cajon', 'objeto']
    search_fields = ['nombre', 'motivo']
    ordering_fields = ['created_at', 'tipo_accion']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtrar historial por usuario autenticado."""
        return Historial.objects.filter(
            usuario=self.request.user,
            is_active=True
        ).select_related('usuario', 'objeto', 'cajon')

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtener estadísticas del historial."""
        queryset = self.get_queryset()
        
        stats = {
            'total_acciones': queryset.count(),
            'acciones_por_tipo': dict(
                queryset.values('tipo_accion').annotate(
                    count=Count('id')
                ).values_list('tipo_accion', 'count')
            ),
            'acciones_ultima_semana': queryset.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count(),
            'objetos_mas_modificados': list(
                queryset.filter(objeto__isnull=False)
                .values('objeto__nombre', 'objeto__id')
                .annotate(count=Count('id'))
                .order_by('-count')[:5]
            )
        }
        
        return Response(stats)


class RecomendacionViewSet(BaseViewSet):
    """
    ViewSet para gestionar recomendaciones.
    """
    serializer_class = RecomendacionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['prioridad', 'tipo_recomendacion', 'implementada']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['fecha_creacion', 'prioridad']
    ordering = ['-fecha_creacion', '-prioridad']

    def get_queryset(self):
        """Filtrar recomendaciones por usuario autenticado."""
        return Recomendacion.objects.filter(
            usuario=self.request.user,
            is_active=True
        ).select_related('usuario')

    def perform_create(self, serializer):
        """Asignar usuario actual al crear recomendación."""
        serializer.save(usuario=self.request.user, user=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_implementada(self, request, pk=None):
        """Marcar recomendación como implementada."""
        recomendacion = self.get_object()
        recomendacion.marcar_como_implementada()
        
        serializer = self.get_serializer(recomendacion)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def desmarcar_implementada(self, request, pk=None):
        """Desmarcar recomendación como implementada."""
        recomendacion = self.get_object()
        recomendacion.desmarcar_implementacion()
        
        serializer = self.get_serializer(recomendacion)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Obtener recomendaciones pendientes ordenadas por prioridad."""
        recomendaciones = self.get_queryset().filter(implementada=False)
        serializer = self.get_serializer(recomendaciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def generar_automaticas(self, request):
        """
        Generar recomendaciones automáticas usando LLM para el usuario autenticado.
        Analiza todos los cajones y objetos del usuario para generar sugerencias inteligentes.
        """
        try:
            # Obtener el ID del usuario desde los parámetros o usar el usuario autenticado
            usuario_id = request.data.get('usuario_id', request.user.id)
            
            # Verificar que el usuario tiene permisos para generar recomendaciones para ese ID
            if usuario_id != request.user.id and not request.user.is_staff:
                return Response(
                    {'error': 'No tienes permisos para generar recomendaciones para otro usuario'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Instanciar el servicio de recomendaciones
            servicio = RecomendacionService()
            
            # Generar recomendaciones
            resultado = servicio.generar_recomendaciones_usuario(usuario_id)
            
            if 'error' in resultado:
                return Response(resultado, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener las recomendaciones recién creadas
            recomendaciones_nuevas = Recomendacion.objects.filter(
                usuario_id=usuario_id,
                is_active=True
            ).order_by('-created_at')[:len(resultado.get('recomendaciones', []))]
            
            # Serializar las recomendaciones
            serializer = self.get_serializer(recomendaciones_nuevas, many=True)
            
            # Agregar información adicional al resultado
            resultado['recomendaciones_guardadas'] = serializer.data
            resultado['total_recomendaciones_generadas'] = len(serializer.data)
            
            return Response(resultado, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error en generar_automaticas: {str(e)}")
            return Response(
                {'error': f'Error interno del servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EstadisticasViewSet(viewsets.ViewSet):
    """
    ViewSet para obtener estadísticas generales del usuario.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def generales(self, request):
        """Obtener estadísticas generales del usuario."""
        usuario = request.user
        
        # Obtener datos base
        cajones = Cajon.objects.filter(usuario=usuario, is_active=True)
        objetos = Objeto.objects.filter(cajon__usuario=usuario, is_active=True)
        recomendaciones = Recomendacion.objects.filter(usuario=usuario, is_active=True)
        ultimo_historial = Historial.objects.filter(usuario=usuario, is_active=True).first()
        
        # Calcular estadísticas
        total_cajones = cajones.count()
        total_objetos = objetos.count()
        cajones_llenos = cajones.filter(objetos__is_active=True).annotate(
            count_objetos=Count('objetos')
        ).filter(count_objetos__gte=models.F('capacidad_maxima')).count()
        
        capacidad_total = sum(cajon.capacidad_maxima for cajon in cajones)
        capacidad_utilizada = total_objetos
        porcentaje_utilizacion = (capacidad_utilizada / capacidad_total * 100) if capacidad_total > 0 else 0
        
        objetos_por_tipo = dict(
            objetos.values('tipo_objeto').annotate(
                count=Count('id')
            ).values_list('tipo_objeto', 'count')
        )
        
        recomendaciones_pendientes = recomendaciones.filter(implementada=False).count()
        
        stats = {
            'total_cajones': total_cajones,
            'total_objetos': total_objetos,
            'objetos_por_tipo': objetos_por_tipo,
            'cajones_llenos': cajones_llenos,
            'capacidad_total': capacidad_total,
            'capacidad_utilizada': capacidad_utilizada,
            'porcentaje_utilizacion': round(porcentaje_utilizacion, 2),
            'recomendaciones_pendientes': recomendaciones_pendientes,
            'ultimo_historial': HistorialSerializer(ultimo_historial).data if ultimo_historial else None
        }
        
        serializer = EstadisticasSerializer(stats)
        return Response(serializer.data)


class ConfiguracionViewSet(viewsets.ViewSet):
    """
    ViewSet para obtener opciones de configuración.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def tipos_objeto(self, request):
        """Obtener todos los tipos de objeto disponibles."""
        tipos = [{'value': choice[0], 'label': choice[1]} for choice in TipoObjeto.choices]
        serializer = TipoObjetoSerializer(tipos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def tamanios(self, request):
        """Obtener todos los tamaños disponibles."""
        tamanios = [{'value': choice[0], 'label': choice[1]} for choice in Tamanio.choices]
        serializer = TamanioSerializer(tamanios, many=True)
        return Response(serializer.data)


class CajonManagementViewSet(viewsets.GenericViewSet):
    """
    ViewSet para gestión avanzada de cajones (eliminar duplicados, ordenar).
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def eliminar_duplicados(self, request):
        """
        Elimina objetos duplicados de un cajón específico.
        
        Body parameters:
        - cajon_id: ID del cajón del cual eliminar duplicados
        """
        from .serializers import EliminarDuplicadosSerializer, AccionResultadoSerializer
        
        serializer = EliminarDuplicadosSerializer(data=request.data)
        if serializer.is_valid():
            cajon_id = serializer.validated_data['cajon_id']
            cajon = get_object_or_404(Cajon, id=cajon_id, usuario=request.user, is_active=True)
            
            # Ejecutar eliminación de duplicados
            duplicados_eliminados = Objeto.eliminar_duplicados_cajon(cajon, request.user)
            
            resultado = {
                'mensaje': f'Se eliminaron {duplicados_eliminados} objetos duplicados',
                'elementos_afectados': duplicados_eliminados,
                'detalles': {
                    'cajon': cajon.nombre,
                    'cajon_id': cajon.id
                }
            }
            
            resultado_serializer = AccionResultadoSerializer(resultado)
            return Response(resultado_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def ordenar_objetos(self, request):
        """
        Ordena los objetos de un cajón según el criterio especificado.
        
        Body parameters:
        - cajon_id: ID del cajón cuyos objetos ordenar
        - criterio: Criterio de ordenamiento ('nombre', 'tipo_objeto', 'peso', 'fecha_ingreso')
        """
        from .serializers import OrdenarObjetosSerializer, AccionResultadoSerializer
        
        serializer = OrdenarObjetosSerializer(data=request.data)
        if serializer.is_valid():
            cajon_id = serializer.validated_data['cajon_id']
            criterio = serializer.validated_data['criterio']
            cajon = get_object_or_404(Cajon, id=cajon_id, usuario=request.user, is_active=True)
            
            # Ejecutar ordenamiento
            objetos_ordenados = Objeto.ordenar_objetos_cajon(cajon, criterio, request.user)
            
            resultado = {
                'mensaje': f'Se ordenaron {len(objetos_ordenados)} objetos por {criterio}',
                'elementos_afectados': len(objetos_ordenados),
                'detalles': {
                    'cajon': cajon.nombre,
                    'cajon_id': cajon.id,
                    'criterio': criterio,
                    'objetos_ordenados': [
                        {
                            'id': obj.id,
                            'nombre': obj.nombre,
                            'tipo_objeto': obj.tipo_objeto,
                            'peso': str(obj.peso)
                        }
                        for obj in objetos_ordenados[:10]  # Mostrar solo los primeros 10
                    ]
                }
            }
            
            resultado_serializer = AccionResultadoSerializer(resultado)
            return Response(resultado_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
