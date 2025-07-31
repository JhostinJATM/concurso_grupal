"""
Serializadores base para la API REST.
Implementa principios SOLID y DRY.
"""
from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField, UUIDField, BooleanField


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Serializador base que incluye campos comunes y validaciones.
    Implementa el principio DRY (Don't Repeat Yourself).
    """
    id = UUIDField(read_only=True)
    created_at = DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_at = DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    is_active = BooleanField(read_only=True)

    class Meta:
        abstract = True
        fields = ['id', 'created_at', 'updated_at', 'is_active']

    def validate(self, attrs):
        """
        Validación personalizada que puede ser extendida por subclases.
        """
        return super().validate(attrs)

    def create(self, validated_data):
        """
        Override create para manejar lógica de negocio común.
        """
        request = self.context.get('request')
        user = None
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        
        instance = self.Meta.model(**validated_data)
        instance.save(user=user)
        return instance

    def update(self, instance, validated_data):
        """
        Override update para manejar lógica de negocio común.
        """
        request = self.context.get('request')
        user = None
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save(user=user)
        return instance


class AuditableModelSerializer(BaseModelSerializer):
    """
    Serializador para modelos auditables.
    Incluye información de creación y modificación.
    """
    created_by = CharField(source='created_by.username', read_only=True)
    updated_by = CharField(source='updated_by.username', read_only=True)

    class Meta:
        abstract = True
        fields = BaseModelSerializer.Meta.fields + ['created_by', 'updated_by']


class DetailSerializer(serializers.Serializer):
    """
    Serializador para respuestas de detalle/mensajes.
    """
    detail = serializers.CharField()
    
    def __init__(self, message="Operación exitosa", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['detail'].default = message
