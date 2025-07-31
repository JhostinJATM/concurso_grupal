
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from core.models import BaseModel, AuditableModel
import uuid


class TipoObjeto(models.TextChoices):
    """
    Enumeración para tipos de objetos.
    Implementa el patrón Value Object del DDD.
    """
    ROPA = 'ROPA', 'Ropa'
    PAPELERIA = 'PAPELERIA', 'Papelería'
    CABLES = 'CABLES', 'Cables'
    ELECTRONICA = 'ELECTRONICA', 'Electrónica'
    LIBROS = 'LIBROS', 'Libros'
    HERRAMIENTAS = 'HERRAMIENTAS', 'Herramientas'
    COCINA = 'COCINA', 'Artículos de Cocina'
    OTROS = 'OTROS', 'Otros'


class Tamanio(models.TextChoices):
    """
    Enumeración para tamaños de objetos.
    Implementa el patrón Value Object del DDD.
    """
    PEQUENO = 'PEQUENO', 'Pequeño'
    MEDIANO = 'MEDIANO', 'Mediano'
    GRANDE = 'GRANDE', 'Grande'


class Cajon(AuditableModel):
    """
    Modelo que representa un cajón en el sistema.
    Hereda de AuditableModel para tener auditoría completa.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre único del cajón",
        validators=[RegexValidator(
            regex=r'^[\w\s\u00C0-\u017F]+$',
            message='Solo se permiten letras, números, espacios y caracteres con tildes'
        )]
    )
    
    capacidad_maxima = models.PositiveIntegerField(
        default=10,
        validators=[
            MinValueValidator(1, message="La capacidad debe ser al menos 1"),
            MaxValueValidator(1000, message="La capacidad no puede exceder 1000")
        ],
        help_text="Capacidad máxima de objetos que puede contener el cajón"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cajones',
        help_text="Usuario propietario del cajón"
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción adicional del cajón"
    )

    class Meta:
        verbose_name = "Cajón"
        verbose_name_plural = "Cajones"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['usuario', 'nombre']),
            models.Index(fields=['capacidad_maxima']),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"
    
    @property
    def objetos_count(self):
        """Cantidad actual de objetos en el cajón."""
        if not self.pk:  # Si el cajón no está guardado aún
            return 0
        return self.objetos.filter(is_active=True).count()
    
    @property
    def capacidad_disponible(self):
        """Capacidad disponible en el cajón."""
        if not self.capacidad_maxima:  # Si no hay capacidad definida
            return 0
        objetos_actuales = self.objetos_count
        return self.capacidad_maxima - objetos_actuales
    
    @property
    def esta_lleno(self):
        """Verifica si el cajón está lleno."""
        if not self.capacidad_maxima:  # Si no hay capacidad definida
            return False
        return self.objetos_count >= self.capacidad_maxima
    
    @property
    def porcentaje_uso(self):
        """Porcentaje de uso del cajón."""
        if not self.capacidad_maxima:
            return 0
        return (self.objetos_count / self.capacidad_maxima) * 100
    
    def clean(self):
        """Validaciones personalizadas del modelo."""
        super().clean()
        if self.capacidad_maxima and self.capacidad_maxima <= 0:
            raise models.ValidationError("La capacidad máxima debe ser mayor que 0")


class Objeto(AuditableModel):
    """
    Modelo que representa un objeto almacenado en un cajón.
    Implementa los métodos de negocio requeridos.
    """
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre del objeto"
    )
    
    tipo_objeto = models.CharField(
        max_length=20,
        choices=TipoObjeto.choices,
        default=TipoObjeto.OTROS,
        help_text="Tipo de objeto"
    )
    
    tamanio = models.CharField(
        max_length=10,
        choices=Tamanio.choices,
        default=Tamanio.MEDIANO,
        help_text="Tamaño del objeto"
    )
    
    cajon = models.ForeignKey(
        Cajon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='objetos',
        help_text="Cajón donde se almacena el objeto"
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción detallada del objeto"
    )
    
    fecha_ingreso = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de ingreso al cajón"
    )

    class Meta:
        verbose_name = "Objeto"
        verbose_name_plural = "Objetos"
        ordering = ['-fecha_ingreso']
        indexes = [
            models.Index(fields=['cajon', 'tipo_objeto']),
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_objeto_display()})"
    
    def clean(self):
        """Validaciones personalizadas del modelo."""
        super().clean()
        
        # Validar que el cajón no esté lleno (solo si hay cajón asignado)
        if self.cajon and self.cajon.esta_lleno:
            # Si estamos actualizando, verificar si es el mismo objeto
            if not self.pk:
                raise models.ValidationError("El cajón seleccionado está lleno")
    
    def save(self, *args, **kwargs):
        """Override save para validaciones antes de guardar."""
        self.full_clean()  # Ejecuta las validaciones
        super().save(*args, **kwargs)
    
    @classmethod
    def nuevo_objeto(cls, **kwargs):
        """
        Método de clase para crear un nuevo objeto.
        Implementa el método nuevoObjeto requerido.
        """
        return cls.objects.create(**kwargs)
    
    def modificar_objeto(self, nombre=None, **info):
        """
        Modifica los atributos del objeto.
        Implementa el método modificarObjeto requerido.
        """
        if nombre:
            self.nombre = nombre
        
        for field, value in info.items():
            if hasattr(self, field):
                setattr(self, field, value)
        
        self.save()
        return self
    
    def eliminar_objeto(self):
        """
        Elimina el objeto (eliminación lógica).
        Implementa el método eliminarObjeto requerido.
        """
        self.soft_delete()
        return self
    
    @classmethod
    def consultar_objeto(cls, nombre=None):
        """
        Consulta objetos por nombre.
        Implementa el método consultarObjeto requerido.
        """
        queryset = cls.objects.filter(is_active=True)
        
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        
        return queryset
    
    @classmethod
    def ordenar_por_tipo(cls):
        """
        Ordena objetos por tipo.
        Implementa el método ordenarTipo requerido.
        """
        return cls.objects.filter(is_active=True).order_by('tipo_objeto', 'nombre')
    
    @classmethod
    def sugerir_tamanio(cls, nombre_objeto):
        """
        Sugiere el tamaño apropiado según el nombre del objeto.
        """
        nombre = nombre_objeto.lower()
        
        # Objetos pequeños típicos
        pequenos = ['llaves', 'monedas', 'usb', 'cable', 'auriculares', 'cargador', 'adaptador']
        # Objetos medianos típicos  
        medianos = ['libro', 'cuaderno', 'mouse', 'teclado', 'camisa', 'pantalon']
        # Objetos grandes típicos
        grandes = ['laptop', 'monitor', 'impresora', 'mochila', 'chaqueta']
        
        for palabra in pequenos:
            if palabra in nombre:
                return Tamanio.PEQUENO
                
        for palabra in medianos:
            if palabra in nombre:
                return Tamanio.MEDIANO
                
        for palabra in grandes:
            if palabra in nombre:
                return Tamanio.GRANDE
        
        return Tamanio.MEDIANO  # Por defecto
    
    def obtener_porcentaje_espacio(self):
        """Obtiene qué porcentaje del cajón ocupa este objeto (siempre 1/capacidad_maxima)."""
        if not self.cajon or not self.cajon.capacidad_maxima:
            return 0
        return (1 / self.cajon.capacidad_maxima) * 100


class Historial(BaseModel):
    """
    Modelo para registrar el historial de acciones del usuario.
    Mantiene un log de todas las operaciones importantes.
    """
    nombre = models.CharField(
        max_length=200,
        help_text="Nombre descriptivo de la acción"
    )
    
    motivo = models.TextField(
        help_text="Motivo o descripción detallada de la acción"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='historial',
        help_text="Usuario que realizó la acción"
    )
    
    objeto = models.ForeignKey(
        Objeto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historial',
        help_text="Objeto relacionado con la acción (opcional)"
    )
    
    cajon = models.ForeignKey(
        Cajon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historial',
        help_text="Cajón relacionado con la acción (opcional)"
    )
    
    tipo_accion = models.CharField(
        max_length=50,
        choices=[
            ('CREAR', 'Crear'),
            ('MODIFICAR', 'Modificar'),
            ('ELIMINAR', 'Eliminar'),
            ('CONSULTAR', 'Consultar'),
            ('MOVER', 'Mover'),
        ],
        default='CREAR',
        help_text="Tipo de acción realizada"
    )

    class Meta:
        verbose_name = "Historial"
        verbose_name_plural = "Historiales"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['usuario', '-created_at']),
            models.Index(fields=['tipo_accion']),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username} ({self.created_at})"


class Recomendacion(BaseModel):
    """
    Modelo para almacenar recomendaciones inteligentes para el usuario.
    Sistema de IA para sugerir optimizaciones.
    """
    nombre = models.CharField(
        max_length=200,
        help_text="Título de la recomendación"
    )
    
    descripcion = models.TextField(
        help_text="Descripción detallada de la recomendación"
    )
    
    fecha_creacion = models.DateField(
        auto_now_add=True,
        help_text="Fecha de creación de la recomendación"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recomendaciones',
        help_text="Usuario destinatario de la recomendación"
    )
    
    prioridad = models.CharField(
        max_length=10,
        choices=[
            ('BAJA', 'Baja'),
            ('MEDIA', 'Media'),
            ('ALTA', 'Alta'),
            ('CRITICA', 'Crítica'),
        ],
        default='MEDIA',
        help_text="Prioridad de la recomendación"
    )
    
    tipo_recomendacion = models.CharField(
        max_length=20,
        choices=[
            ('ORGANIZACION', 'Organización'),
            ('ESPACIO', 'Optimización de Espacio'),
            ('MANTENIMIENTO', 'Mantenimiento'),
            ('SEGURIDAD', 'Seguridad'),
            ('EFICIENCIA', 'Eficiencia'),
        ],
        default='ORGANIZACION',
        help_text="Tipo de recomendación"
    )
    
    implementada = models.BooleanField(
        default=False,
        help_text="Indica si la recomendación ha sido implementada"
    )
    
    fecha_implementacion = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha en que se implementó la recomendación"
    )

    class Meta:
        verbose_name = "Recomendación"
        verbose_name_plural = "Recomendaciones"
        ordering = ['-fecha_creacion', '-prioridad']
        indexes = [
            models.Index(fields=['usuario', '-fecha_creacion']),
            models.Index(fields=['prioridad']),
            models.Index(fields=['implementada']),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"
    
    def marcar_como_implementada(self):
        """Marca la recomendación como implementada."""
        self.implementada = True
        self.fecha_implementacion = timezone.now()
        self.save(update_fields=['implementada', 'fecha_implementacion'])
    
    def desmarcar_implementacion(self):
        """Desmarca la recomendación como implementada."""
        self.implementada = False
        self.fecha_implementacion = None
        self.save(update_fields=['implementada', 'fecha_implementacion'])
