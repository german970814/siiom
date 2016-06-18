# Django Package
from django import forms
from django.utils.translation import ugettext_lazy as _

# Locale Apps
from .models import Registro, Documento

# Apss
from organizacional.models import Departamento


class FormularioRegistroDocumento(forms.ModelForm):
    """
    alsda
    """
    error_css_class = 'has-error'

    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), label='Departamento')
    palabras = forms.CharField(max_length=255, label='Palabras Claves', required=False)

    class Meta:
        model = Registro
        exclude = ('palabras_claves', )

    def __init__(self, *args, **kwargs):
        super(FormularioRegistroDocumento, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = _(self.fields[field].label)
            if field == 'area' or field == 'departamento':
                self.fields[field].widget.attrs.update({'class': 'selectpicker'})
                continue
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class FormularioDocumentos(forms.ModelForm):
    """"""

    error_css_class = 'has-error'

    class Meta:
        model = Documento
        exclude = ('registro', )

    def __init__(self, *args, **kwargs):
        super(FormularioDocumentos, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = _(self.fields[field].label)
            self.fields[field].widget.attrs.update({'class': 'form-control'})

            if field == 'archivo':
                self.fields[field].widget.attrs.update({'accept': 'image/*'})
