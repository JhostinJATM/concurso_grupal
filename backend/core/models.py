"""
Modelos base siguiendo principios DDD y Clean Architecture.
"""
from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """
    Modelo base que implementa campos comunes para todas las entidades.
    Sigue principios de DDD (Domain-Driven Design).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador único universal"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de última actualización"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si el registro está activo"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"

    def soft_delete(self):
        """Eliminación lógica del registro."""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])

    def restore(self):
        """Restaurar un registro eliminado lógicamente."""
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])


class AuditableModel(BaseModel):
    """
    Modelo base que incluye campos de auditoría.
    Extiende BaseModel con información de quién creó/modificó.
    """
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        null=True,
        blank=True,
        help_text="Usuario que creó el registro"
    )
    
    updated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT,
        related_name='%(class)s_updated',
        null=True,
        blank=True,
        help_text="Usuario que actualizó el registro por última vez"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Override save para manejar auditoría automática."""
        user = kwargs.pop('user', None)
        
        if user:
            if not self.pk:  # Nuevo registro
                self.created_by = user
            self.updated_by = user
            
        super().save(*args, **kwargs)
