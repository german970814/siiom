from django import forms
from django.utils.translation import ugettext_lazy as _

from grupos.models import Grupo
from miembros.models import Miembro
from .models import Materia, Modulo, Sesion
from common.forms import CustomModelForm, CustomForm
from . import resources


class MateriaForm(CustomModelForm):
    """
    Formulario para crear las Materias.
    """

    class Meta:
        model = Materia
        fields = ('nombre', 'grupos_minimo', 'dependencia', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['grupos_minimo'].widget.attrs.update({'class': 'form-control'})
        self.fields['dependencia'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})


class PrioridadMixin:
    OBJETO = _('')

    error_messages = {
        'prioridad_exists': _('Ya existe un %s con esta prioridad.' % OBJETO)
    }


class ModuloForm(PrioridadMixin, CustomModelForm):
    """
    Formulario para crear los módulos de cada materia.
    """

    OBJETO = _('módulo')

    class Meta:
        model = Modulo
        fields = ('nombre', 'prioridad', )

    def __init__(self, materia=None, *args, **kwargs):
        self.materia = materia
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioridad'].widget.attrs.update({'class': 'form-control'})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)

        if self.materia is not None:
            if 'prioridad' in cleaned_data and self.materia.modulos.filter(prioridad=cleaned_data.get('prioridad')).exists():
                self.add_error(
                    'prioridad',
                    forms.ValidationError(self.error_messages['prioridad_exists'], code='prioridad_exists')
                )
        else:
            if self.instance.materia.modulos.filter(
               prioridad=cleaned_data.get('prioridad')).exclude(id=self.instance.id).exists():
                self.add_error(
                    'prioridad',
                    forms.ValidationError(self.error_messages['prioridad_exists'], code='prioridad_exists')
                )
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        if commit and self.materia is not None:
            self.instance.materia = self.materia
        return super().save(commit=commit, *args, **kwargs)


class SesionForm(PrioridadMixin, CustomModelForm):
    """
    Formulario para crear una sesión.
    """

    OBJETO = _('sesión')

    class Meta:
        model = Sesion
        fields = ('nombre', 'prioridad', )

    def __init__(self, modulo=None, *args, **kwargs):
        self.modulo = modulo
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioridad'].widget.attrs.update({'class': 'form-control'})

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)

        if self.modulo is not None:
            if 'prioridad' in cleaned_data and self.modulo.sesiones.filter(prioridad=cleaned_data.get('prioridad')).exists():
                self.add_error(
                    'prioridad',
                    forms.ValidationError(self.error_messages['prioridad_exists'], code='prioridad_exists')
                )
        else:
            if self.instance.modulo.sesiones.filter(
               prioridad=cleaned_data.get('prioridad')).exclude(id=self.instance.id).exists():
                self.add_error(
                    'prioridad',
                    forms.ValidationError(self.error_messages['prioridad_exists'], code='prioridad_exists')
                )
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        if commit and self.modulo is not None:
            self.instance.modulo = self.modulo
        return super().save(commit=commit, *args, **kwargs)


class ReporteInstitutoForm(CustomForm):
    
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.prefetch_related('lideres').all(), label=_('Grupo'))
    materias = forms.ModelMultipleChoiceField(queryset=Materia.objects.all(), label=_('Materias'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo'].widget.attrs.update({'class': self.select_css_class, 'data-live-search': 'true'})
        self.fields['materias'].widget.attrs.update({'class': 'chosen', 'placeholder': 'Escoge algunas materias'})

    def get_lideres(self):
        if self.is_bound and not bool(self._errors):
            grupo = self.cleaned_data.get('grupo')
            grupos = grupo._grupos_red.prefetch_related('lideres')
            lideres = Miembro.objects.filter(id__in=grupos.values_list('lideres__id', flat=True))
            return lideres
        return Miembro.objects.none()

    def get_materias(self):
        if self.is_bound and not bool(self._errors):
            materias = self.cleaned_data.get('materias')
            if not materias.exists():
                materias = Materia.objects.all()
            return materias
        return Materia.objects.none()

    def get_excel(self):
        lideres = self.get_lideres()
        materias = self.get_materias()
        return resources.ReporteInstituto(data=lideres, materias=materias)
