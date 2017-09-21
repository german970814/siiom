from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import CustomModelForm
from .models import Materia, Modulo, Sesion


class FormularioMateria(CustomModelForm):
    """
    Formulario para crear las Materias.
    """

    class Meta:
        model = Materia
        fields = ('nombre', 'grupos_minimo', 'dependencia', )


class PrioridadMixin:
    OBJETO = _('')

    error_messages = {
        'prioridad_exists': _('Ya existe un %s con esta prioridad.' % OBJETO)
    }


class FormularioModulo(PrioridadMixin, CustomModelForm):
    """
    Formulario para crear los módulos de cada materia.
    """

    OBJETO = _('módulo')

    class Meta:
        model = Modulo
        fields = ('nombre', 'prioridad', 'materia', )

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)

        if 'materia' in cleaned_data and 'prioridad' in cleaned_data:
            if cleaned_data.get('materia').modulos.filter(prioridad=cleaned_data.get('prioridad')).exists():
                self.add_error(
                    'prioridad',
                    forms.ValidationError(self.error_messages['prioridad_exists'], code='prioridad_exists')
                )
        return cleaned_data


class FormularioSesion(PrioridadMixin, CustomModelForm):
    """
    Formulario para crear una sesión.
    """

    OBJETO = _('sesión')

    class Meta:
        model = Sesion
        fields = ('nombre', 'prioridad', 'modulo')
