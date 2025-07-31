"""
Validadores personalizados para el sistema.
Implementa principios SOLID y Clean Code.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class BaseValidator:
    """
    Validador base que implementa el patrón Strategy.
    """
    message = _('Valor inválido.')
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        """
        Implementar en subclases.
        """
        raise NotImplementedError

    def clean(self, value):
        """
        Limpiar el valor antes de validar.
        """
        return value


class AlphanumericValidator(BaseValidator):
    """
    Validador para cadenas alfanuméricas.
    """
    regex = re.compile(r'^[a-zA-Z0-9]+$')
    message = _('Solo se permiten caracteres alfanuméricos.')
    code = 'alphanumeric'

    def __call__(self, value):
        if not self.regex.match(str(value)):
            raise ValidationError(self.message, code=self.code)


class PhoneNumberValidator(BaseValidator):
    """
    Validador para números de teléfono.
    """
    regex = re.compile(r'^\+?1?\d{9,15}$')
    message = _('Número de teléfono inválido.')
    code = 'invalid_phone'

    def __call__(self, value):
        cleaned_value = re.sub(r'[\s\-\(\)]', '', str(value))
        if not self.regex.match(cleaned_value):
            raise ValidationError(self.message, code=self.code)


class PositiveNumberValidator(BaseValidator):
    """
    Validador para números positivos.
    """
    message = _('El valor debe ser un número positivo.')
    code = 'not_positive'

    def __call__(self, value):
        try:
            num_value = float(value)
            if num_value <= 0:
                raise ValidationError(self.message, code=self.code)
        except (ValueError, TypeError):
            raise ValidationError(_('Debe ser un número válido.'), code='invalid_number')


class UniqueFieldValidator:
    """
    Validador para verificar unicidad de campos.
    Implementa el principio de responsabilidad única.
    """
    def __init__(self, model, field, exclude_pk=None, message=None):
        self.model = model
        self.field = field
        self.exclude_pk = exclude_pk
        self.message = message or _('Este valor ya existe.')

    def __call__(self, value):
        queryset = self.model.objects.filter(**{self.field: value})
        
        if self.exclude_pk:
            queryset = queryset.exclude(pk=self.exclude_pk)
            
        if queryset.exists():
            raise ValidationError(self.message, code='unique')


def validate_drawer_code(value):
    """
    Validador específico para códigos de cajones.
    """
    if not re.match(r'^DRW-[A-Z0-9]{6}$', value):
        raise ValidationError(
            _('El código del cajón debe tener el formato DRW-XXXXXX'),
            code='invalid_drawer_code'
        )


def validate_sensor_id(value):
    """
    Validador específico para IDs de sensores.
    """
    if not re.match(r'^SEN-[0-9]{8}$', value):
        raise ValidationError(
            _('El ID del sensor debe tener el formato SEN-XXXXXXXX'),
            code='invalid_sensor_id'
        )
