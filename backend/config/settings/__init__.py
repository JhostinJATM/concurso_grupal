"""
Archivo de configuración principal de settings.
Determina qué configuración usar basado en la variable de entorno DJANGO_SETTINGS_MODULE.
"""

import os

# Determinar el entorno
ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'testing':
    from .testing import *
else:
    from .development import *
