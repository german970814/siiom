from django import forms
from django.utils.translation import ugettext_lazy as _


class FormularioRangoFechas(forms.Form):
    """
    Formulario de base para rangos de fechas
    """
    error_css_class = 'has-error'

    fecha_inicial = forms.DateField(label=_('Fecha Inicial'))
    fecha_final = forms.DateField(label=_('Fecha Final'))

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['fecha_inicial'].widget.attrs.update(
            {'class': 'form-control', 'data-mask': '00/00/00'}
        )
        self.fields['fecha_final'].widget.attrs.update(
            {'class': 'form-control', 'data-mask': '00/00/00'}
        )

    def clean(self, *args, **kwargs):
        cleaned_data = super(self.__class__, self).clean(*args, **kwargs)

        fechas = (cleaned_data.get('fecha_inicial', None), cleaned_data.get('fecha_final', None))

        if all(fechas):
            if fechas[0] > fechas[1]:
                self.add_error('fecha_inicial', _('Fecha inicial no puede ser mayor que Fecha Final'))
                self.add_error('fecha_final', _('Fecha final no puede ser menor que Fecha Inicial'))
