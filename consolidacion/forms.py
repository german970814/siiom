from django import forms

from .models import Visita
from grupos.models import Grupo


class BaseModelForm(forms.ModelForm):
    """
    Formulario base para los formularios
    """

    error_css_class = 'has-error'


class FormularioVisita(BaseModelForm):
    class Meta:
        model = Visita
        fields = (
            'primer_nombre', 'segundo_nombre', 'primer_apellido',
            'segundo_apellido', 'direccion', 'telefono', 'email', 'genero'
        )

    def __init__(self, *args, **kwargs):
        super(FormularioVisita, self).__init__(*args, **kwargs)
        self.fields['primer_nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['segundo_nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['primer_apellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['segundo_apellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['genero'].widget.attrs.update({'class': 'selectpicker'})


class FormularioAsignarGrupoVisita(forms.Form):
    """
    Formulario de Asignacion de visita a grupo
    """

    visita = forms.ModelChoiceField(queryset=Visita.objects.filter(retirado=False))
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.activos())

    def __init__(self, *args, **kwargs):
        super(FormularioAsignarGrupoVisita, self).__init__(*args, **kwargs)
