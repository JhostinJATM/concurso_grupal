"""
Utilidades generales del sistema.
"""
import uuid
import hashlib
from datetime import datetime, timedelta
from django.utils import timezone
from typing import Optional, Dict, Any


def generate_unique_code(prefix: str = "", length: int = 8) -> str:
    """
    Genera un código único con un prefijo opcional.
    
    Args:
        prefix: Prefijo para el código
        length: Longitud del código (sin incluir el prefijo)
    
    Returns:
        Código único generado
    """
    unique_id = str(uuid.uuid4()).replace('-', '').upper()[:length]
    return f"{prefix}{unique_id}" if prefix else unique_id


def generate_hash(data: str, algorithm: str = 'sha256') -> str:
    """
    Genera un hash de los datos proporcionados.
    
    Args:
        data: Datos a hashear
        algorithm: Algoritmo de hash a usar
    
    Returns:
        Hash generado
    """
    hash_object = hashlib.new(algorithm)
    hash_object.update(data.encode('utf-8'))
    return hash_object.hexdigest()


def calculate_time_difference(start_time: datetime, end_time: datetime = None) -> Dict[str, int]:
    """
    Calcula la diferencia entre dos fechas.
    
    Args:
        start_time: Fecha de inicio
        end_time: Fecha de fin (por defecto, ahora)
    
    Returns:
        Diccionario con la diferencia en días, horas, minutos y segundos
    """
    if end_time is None:
        end_time = timezone.now()
    
    diff = end_time - start_time
    
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'total_seconds': int(diff.total_seconds())
    }


def format_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
    """
    Formatea una respuesta estándar para la API.
    
    Args:
        data: Datos a incluir en la respuesta
        message: Mensaje descriptivo
        status_code: Código de estado HTTP
    
    Returns:
        Diccionario con la respuesta formateada
    """
    response = {
        'status_code': status_code,
        'message': message,
        'timestamp': timezone.now().isoformat(),
    }
    
    if data is not None:
        response['data'] = data
    
    return response


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza un nombre de archivo removiendo caracteres peligrosos.
    
    Args:
        filename: Nombre del archivo a sanitizar
    
    Returns:
        Nombre del archivo sanitizado
    """
    import re
    # Remover caracteres peligrosos
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remover espacios múltiples y reemplazar por guion bajo
    sanitized = re.sub(r'\s+', '_', sanitized)
    # Limitar longitud
    return sanitized[:255]


def chunks(lst: list, n: int):
    """
    Divide una lista en chunks de tamaño n.
    
    Args:
        lst: Lista a dividir
        n: Tamaño de cada chunk
    
    Yields:
        Chunks de la lista
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class SingletonMeta(type):
    """
    Metaclass para implementar el patrón Singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
