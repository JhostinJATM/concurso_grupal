"""
Configuración del admin para Cajones Inteligentes.
"""
from django.contrib import admin
from .models import Cajon, Objeto, Historial, Recomendacion


@admin.register(Cajon)
class CajonAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Cajón.
    """
    list_display = ['nombre', 'usuario', 'capacidad_maxima', 'get_objetos_count', 'get_capacidad_disponible', 'get_esta_lleno', 'is_active']
    list_filter = ['usuario', 'capacidad_maxima', 'is_active', 'created_at']
    search_fields = ['nombre', 'descripcion', 'usuario__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']
    filter_horizontal = []
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'usuario', 'capacidad_maxima')
        }),
        ('Detalles', {
            'fields': ('descripcion',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Auditoría', {
            'fields': ('id', 'created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        })
    )

    def get_objetos_count(self, obj):
        """Mostrar cantidad de objetos."""
        if not obj.pk:  # Si es un objeto nuevo
            return "Guarde primero para ver estadísticas"
        return obj.objetos_count
    get_objetos_count.short_description = 'Objetos'

    def get_capacidad_disponible(self, obj):
        """Mostrar capacidad disponible."""
        if not obj.pk:  # Si es un objeto nuevo
            return "Guarde primero para ver estadísticas"
        return obj.capacidad_disponible
    get_capacidad_disponible.short_description = 'Capacidad Disponible'
    
    def get_esta_lleno(self, obj):
        """Mostrar si el cajón está lleno."""
        if not obj.pk:  # Si es un objeto nuevo
            return None
        return obj.esta_lleno
    get_esta_lleno.short_description = 'Lleno'
    get_esta_lleno.boolean = True


@admin.register(Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Objeto.
    """
    list_display = ['nombre', 'tipo_objeto', 'tamanio', 'get_porcentaje_espacio', 'cajon', 'fecha_ingreso', 'is_active']
    list_filter = ['tipo_objeto', 'tamanio', 'cajon', 'is_active', 'fecha_ingreso']
    search_fields = ['nombre', 'descripcion', 'cajon__nombre']
    readonly_fields = ['id', 'created_at', 'updated_at', 'fecha_ingreso', 'created_by', 'updated_by']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo_objeto', 'tamanio')
        }),
        ('Ubicación', {
            'fields': ('cajon',)
        }),
        ('Detalles', {
            'fields': ('descripcion',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Auditoría', {
            'fields': ('id', 'fecha_ingreso', 'created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        })
    )

    def get_porcentaje_espacio(self, obj):
        """Mostrar porcentaje de espacio que ocupa el objeto."""
        if obj.cajon:
            porcentaje = obj.obtener_porcentaje_espacio()
            return f"{porcentaje:.1f}%"
        return "N/A"
    get_porcentaje_espacio.short_description = '% Espacio'


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Historial.
    """
    list_display = ['nombre', 'tipo_accion', 'usuario', 'objeto', 'cajon', 'created_at']
    list_filter = ['tipo_accion', 'usuario', 'created_at']
    search_fields = ['nombre', 'motivo', 'usuario__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo_accion', 'motivo')
        }),
        ('Relaciones', {
            'fields': ('usuario', 'objeto', 'cajon')
        }),
        ('Auditoría', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Recomendación.
    """
    list_display = [
        'nombre', 'tipo_recomendacion', 'prioridad', 'usuario', 
        'implementada', 'fecha_creacion'
    ]
    list_filter = [
        'tipo_recomendacion', 'prioridad', 'implementada', 
        'fecha_creacion', 'usuario'
    ]
    search_fields = ['nombre', 'descripcion', 'usuario__username']
    readonly_fields = ['id', 'fecha_creacion', 'created_at', 'updated_at']
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo_recomendacion', 'prioridad')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'usuario')
        }),
        ('Estado', {
            'fields': ('implementada', 'fecha_implementacion')
        }),
        ('Auditoría', {
            'fields': ('id', 'fecha_creacion', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    actions = ['marcar_como_implementada', 'desmarcar_implementacion']

    def marcar_como_implementada(self, request, queryset):
        """Acción para marcar recomendaciones como implementadas."""
        count = 0
        for recomendacion in queryset:
            if not recomendacion.implementada:
                recomendacion.marcar_como_implementada()
                count += 1
        
        self.message_user(
            request,
            f"{count} recomendaciones marcadas como implementadas."
        )
    marcar_como_implementada.short_description = "Marcar como implementadas"

    def desmarcar_implementacion(self, request, queryset):
        """Acción para desmarcar recomendaciones como implementadas."""
        count = 0
        for recomendacion in queryset:
            if recomendacion.implementada:
                recomendacion.desmarcar_implementacion()
                count += 1
        
        self.message_user(
            request,
            f"{count} recomendaciones desmarcadas como implementadas."
        )
    desmarcar_implementacion.short_description = "Desmarcar implementación"