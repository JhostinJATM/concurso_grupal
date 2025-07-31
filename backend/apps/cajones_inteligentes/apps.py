"""
Configuración de la aplicación Cajones Inteligentes.
"""
from django.apps import AppConfig


class CajonesInteligentesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cajones_inteligentes'
    verbose_name = 'Cajones Inteligentes'
    
    def ready(self):
        """
        Configuración que se ejecuta cuando la aplicación está lista.
        """
        pass
