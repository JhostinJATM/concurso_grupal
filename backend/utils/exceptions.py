"""
Excepciones personalizadas para el sistema.
Implementa principios de Clean Code para manejo de errores.
"""
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response


class SmartDrawersException(Exception):
    """
    Excepción base para el sistema Smart Drawers.
    """
    default_message = "Ha ocurrido un error en el sistema"
    default_code = "SMART_DRAWERS_ERROR"
    
    def __init__(self, message=None, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(SmartDrawersException):
    """
    Excepción para errores de validación.
    """
    default_message = "Error de validación"
    default_code = "VALIDATION_ERROR"


class BusinessLogicException(SmartDrawersException):
    """
    Excepción para errores de lógica de negocio.
    """
    default_message = "Error en la lógica de negocio"
    default_code = "BUSINESS_LOGIC_ERROR"


class ResourceNotFoundException(SmartDrawersException):
    """
    Excepción para recursos no encontrados.
    """
    default_message = "Recurso no encontrado"
    default_code = "RESOURCE_NOT_FOUND"
    
    def __init__(self, message=None, code=None):
        super().__init__(message, code, status.HTTP_404_NOT_FOUND)


class PermissionDeniedException(SmartDrawersException):
    """
    Excepción para permisos denegados.
    """
    default_message = "No tiene permisos para realizar esta acción"
    default_code = "PERMISSION_DENIED"
    
    def __init__(self, message=None, code=None):
        super().__init__(message, code, status.HTTP_403_FORBIDDEN)


def custom_exception_handler(exc, context):
    """
    Manejador personalizado de excepciones para DRF.
    """
    # Llamar al manejador por defecto primero
    response = exception_handler(exc, context)
    
    # Si es una excepción personalizada, formatear la respuesta
    if isinstance(exc, SmartDrawersException):
        custom_response_data = {
            'error': {
                'code': exc.code,
                'message': exc.message,
                'status_code': exc.status_code
            }
        }
        return Response(custom_response_data, status=exc.status_code)
    
    # Para otras excepciones, mantener el formato estándar
    return response
