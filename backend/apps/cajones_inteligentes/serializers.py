"""
Serializadores para la aplicación de Cajones Inteligentes.
Implementa principios SOLID y Clean Code para la API REST.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from core.serializers import BaseModelSerializer, AuditableModelSerializer
from .models import Cajon, Objeto, Historial, Recomendacion, TipoObjeto, Tamanio


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User de Django.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        """Obtiene el nombre completo del usuario."""
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class CajonSerializer(AuditableModelSerializer):
    """
    Serializador para el modelo Cajón.
    """
    objetos_count = serializers.ReadOnlyField()
    capacidad_disponible = serializers.ReadOnlyField()
    esta_lleno = serializers.ReadOnlyField()
    porcentaje_uso = serializers.ReadOnlyField()
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)
    
    class Meta:
        model = Cajon
        fields = AuditableModelSerializer.Meta.fields + [
            'nombre', 'capacidad_maxima', 'usuario', 'usuario_info',
            'descripcion', 'objetos_count', 'capacidad_disponible', 
            'esta_lleno', 'porcentaje_uso'
        ]
        read_only_fields = AuditableModelSerializer.Meta.fields + [
            'usuario', 'objetos_count', 'capacidad_disponible', 'esta_lleno', 'porcentaje_uso'
        ]
    
    def validate_capacidad_maxima(self, value):
        """Validación personalizada para capacidad máxima."""
        if value <= 0:
            raise serializers.ValidationError("La capacidad máxima debe ser mayor que 0")
        if value > 1000:
            raise serializers.ValidationError("La capacidad máxima no puede exceder 1000")
        return value
    
    def validate_nombre(self, value):
        """Validación personalizada para el nombre."""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        return value.strip()
    
    def create(self, validated_data):
        """Override create para manejar el usuario correctamente."""
        request = self.context.get('request')
        user = None
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        
        # El usuario se pasará en el save() como parámetro adicional
        cajon = Cajon(**validated_data)
        cajon.save(user=user)
        return cajon


class CajonListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listado de cajones.
    """
    objetos_count = serializers.ReadOnlyField()
    esta_lleno = serializers.ReadOnlyField()
    
    class Meta:
        model = Cajon
        fields = ['id', 'nombre', 'capacidad_maxima', 'objetos_count', 'esta_lleno']


class ObjetoSerializer(AuditableModelSerializer):
    """
    Serializador para el modelo Objeto.
    """
    cajon_info = CajonListSerializer(source='cajon', read_only=True)
    tipo_objeto_display = serializers.CharField(source='get_tipo_objeto_display', read_only=True)
    tamanio_display = serializers.CharField(source='get_tamanio_display', read_only=True)
    porcentaje_espacio = serializers.SerializerMethodField()
    
    class Meta:
        model = Objeto
        fields = AuditableModelSerializer.Meta.fields + [
            'nombre', 'tipo_objeto', 'tipo_objeto_display',
            'tamanio', 'tamanio_display', 'cajon', 'cajon_info',
            'descripcion', 'fecha_ingreso', 'porcentaje_espacio'
        ]
        read_only_fields = AuditableModelSerializer.Meta.fields + [
            'fecha_ingreso', 'tipo_objeto_display', 'tamanio_display', 'porcentaje_espacio'
        ]
    
    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_porcentaje_espacio(self, obj):
        """Obtiene el porcentaje de espacio del objeto respecto al cajón."""
        return obj.obtener_porcentaje_espacio()
    
    def validate(self, attrs):
        """Validación completa del objeto."""
        attrs = super().validate(attrs)
        
        # Validar que el cajón pertenezca al usuario actual
        cajon = attrs.get('cajon')
        if cajon:
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                if cajon.usuario != request.user:
                    raise serializers.ValidationError({
                        'cajon': 'No puedes asignar objetos a cajones que no te pertenecen'
                    })
        
        # Validar que el cajón no esté lleno (solo si se proporciona un cajón)
        if cajon and cajon.esta_lleno:
            # Si estamos actualizando, verificar si es el mismo objeto
            if not self.instance or self.instance.cajon != cajon:
                raise serializers.ValidationError({
                    'cajon': 'El cajón seleccionado está lleno'
                })
        
        return attrs
    
    def validate_nombre(self, value):
        """Validación personalizada para el nombre."""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        return value.strip()


class ObjetoListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listado de objetos.
    """
    tipo_objeto_display = serializers.CharField(source='get_tipo_objeto_display', read_only=True)
    tamanio_display = serializers.CharField(source='get_tamanio_display', read_only=True)
    cajon_nombre = serializers.CharField(source='cajon.nombre', read_only=True)
    
    class Meta:
        model = Objeto
        fields = [
            'id', 'nombre', 'tipo_objeto', 'tipo_objeto_display',
            'tamanio', 'tamanio_display', 'cajon_nombre', 'fecha_ingreso'
        ]


class HistorialSerializer(BaseModelSerializer):
    """
    Serializador para el modelo Historial.
    """
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)
    objeto_info = ObjetoListSerializer(source='objeto', read_only=True)
    cajon_info = CajonListSerializer(source='cajon', read_only=True)
    tipo_accion_display = serializers.CharField(source='get_tipo_accion_display', read_only=True)
    
    class Meta:
        model = Historial
        fields = BaseModelSerializer.Meta.fields + [
            'nombre', 'motivo', 'usuario', 'usuario_info',
            'objeto', 'objeto_info', 'cajon', 'cajon_info',
            'tipo_accion', 'tipo_accion_display'
        ]
        read_only_fields = BaseModelSerializer.Meta.fields + ['tipo_accion_display']
    
    def validate_motivo(self, value):
        """Validación personalizada para el motivo."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El motivo debe tener al menos 5 caracteres")
        return value.strip()


class RecomendacionSerializer(BaseModelSerializer):
    """
    Serializador para el modelo Recomendación.
    """
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)
    prioridad_display = serializers.CharField(source='get_prioridad_display', read_only=True)
    tipo_recomendacion_display = serializers.CharField(source='get_tipo_recomendacion_display', read_only=True)
    dias_desde_creacion = serializers.SerializerMethodField()
    
    class Meta:
        model = Recomendacion
        fields = BaseModelSerializer.Meta.fields + [
            'nombre', 'descripcion', 'fecha_creacion', 'usuario', 'usuario_info',
            'prioridad', 'prioridad_display', 'tipo_recomendacion', 
            'tipo_recomendacion_display', 'implementada', 'fecha_implementacion',
            'dias_desde_creacion'
        ]
        read_only_fields = BaseModelSerializer.Meta.fields + [
            'fecha_creacion', 'prioridad_display', 'tipo_recomendacion_display',
            'dias_desde_creacion'
        ]
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_dias_desde_creacion(self, obj):
        """Calcula los días desde la creación de la recomendación."""
        from django.utils import timezone
        delta = timezone.now().date() - obj.fecha_creacion
        return delta.days
    
    def validate_descripcion(self, value):
        """Validación personalizada para la descripción."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres")
        return value.strip()


class EstadisticasSerializer(serializers.Serializer):
    """
    Serializador para estadísticas del usuario.
    """
    total_cajones = serializers.IntegerField()
    total_objetos = serializers.IntegerField()
    objetos_por_tipo = serializers.DictField()
    cajones_llenos = serializers.IntegerField()
    peso_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    peso_utilizado = serializers.DecimalField(max_digits=10, decimal_places=2)
    porcentaje_utilizacion = serializers.FloatField()


class EliminarDuplicadosSerializer(serializers.Serializer):
    """
    Serializador para la acción de eliminar duplicados.
    """
    cajon_id = serializers.IntegerField()
    
    def validate_cajon_id(self, value):
        """Validar que el cajón existe."""
        try:
            cajon = Cajon.objects.get(id=value, is_active=True)
            return value
        except Cajon.DoesNotExist:
            raise serializers.ValidationError("El cajón especificado no existe.")


class OrdenarObjetosSerializer(serializers.Serializer):
    """
    Serializador para la acción de ordenar objetos.
    """
    cajon_id = serializers.IntegerField()
    criterio = serializers.ChoiceField(
        choices=[
            ('nombre', 'Nombre'),
            ('tipo_objeto', 'Tipo de Objeto'),
            ('peso', 'Peso'),
            ('fecha_ingreso', 'Fecha de Ingreso')
        ],
        default='nombre'
    )
    
    def validate_cajon_id(self, value):
        """Validar que el cajón existe."""
        try:
            cajon = Cajon.objects.get(id=value, is_active=True)
            return value
        except Cajon.DoesNotExist:
            raise serializers.ValidationError("El cajón especificado no existe.")


class AccionResultadoSerializer(serializers.Serializer):
    """
    Serializador para los resultados de las acciones.
    """
    mensaje = serializers.CharField()
    elementos_afectados = serializers.IntegerField()
    detalles = serializers.DictField(required=False)
    recomendaciones_pendientes = serializers.IntegerField()
    ultimo_historial = HistorialSerializer(read_only=True)


class TipoObjetoSerializer(serializers.Serializer):
    """
    Serializador para los tipos de objeto (choices).
    """
    value = serializers.CharField()
    label = serializers.CharField()


class TamanioSerializer(serializers.Serializer):
    """
    Serializador para los tamaños (choices).
    """
    value = serializers.CharField()
    label = serializers.CharField()
