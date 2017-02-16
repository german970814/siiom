from django import forms
from django.forms.utils import ErrorList
from django.utils.encoding import force_text
from django.utils.html import format_html_join
from django.utils.translation import ugettext_lazy as _lazy
from django.utils.module_loading import import_string


class CustomErrorList(ErrorList):

    def __str__(self):
        return self.as_material()

    def as_material(self):
        if not self.data:
            return ''

        return format_html_join('', '<small class="help-block">{}</small>', ((force_text(e),) for e in self))


class CustomModelForm(forms.ModelForm):
    """
    Formulario base para ModelForm.
    """

    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)


class CustomForm(forms.Form):
    """
    Formulario base para Form.
    """

    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super().__init__(error_class=CustomErrorList, *args, **kwargs)


class FormularioRangoFechas(CustomForm):
    """
    Formulario base para rangos de fechas.
    """

    fecha_inicial = forms.DateField(label=_lazy('Fecha Inicial'))
    fecha_final = forms.DateField(label=_lazy('Fecha Final'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicial'].widget.attrs.update(
            {'class': 'form-control', 'data-mask': '00/00/00'}
        )
        self.fields['fecha_final'].widget.attrs.update(
            {'class': 'form-control', 'data-mask': '00/00/00'}
        )

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)

        fechas = (cleaned_data.get('fecha_inicial', None), cleaned_data.get('fecha_final', None))

        if all(fechas):
            if fechas[0] > fechas[1]:
                self.add_error('fecha_inicial', _lazy('Fecha inicial no puede ser mayor que Fecha Final'))
                self.add_error('fecha_final', _lazy('Fecha final no puede ser menor que Fecha Inicial'))


class BusquedaForm(forms.Form):
    """Formulario de busqueda."""

    Grupo = import_string('grupos.models.Grupo')
    value = forms.CharField(max_length=255)
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=False)
    grupo_by = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=False)
