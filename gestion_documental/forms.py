# Django Package
from django import forms
from django.utils.translation import ugettext_lazy as _

# Locale Apps
from .models import Registro, Documento, TipoDocumento, PalabraClave

# Apss
from organizacional.models import Departamento, Area


class FormularioRegistroDocumento(forms.ModelForm):
    """
    Formulario para el modelo de registro en el capture
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
                self.fields[field].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
                continue
            if field == 'descripcion':
                self.fields[field].widget.attrs.update({'rows': '5'})
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['area'].queryset = Area.objects.none()

        if self.is_bound:
            id_area = self.data.get('area', None)
            try:
                self.fields['area'].queryset = Area.objects.filter(id=id_area)
            except:
                self.fields['area'].queryset = Area.objects.none()


class FormularioDocumentos(forms.ModelForm):
    """
    Formulario para el modelo de documentos
    """

    error_css_class = 'has-error'

    class Meta:
        model = Documento
        exclude = ('registro', )

    def __init__(self, *args, **kwargs):
        super(FormularioDocumentos, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = _(self.fields[field].label)
            if field == 'archivo':
                self.fields[field].widget.attrs.update({'accept': 'image/*,.pdf'})
                continue
            if field == 'tipo_documento':
                self.fields[field].widget.attrs.update({'class': 'form-control tipo_doc', 'data-live-search': 'true'})
                continue
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['tipo_documento'].queryset = TipoDocumento.objects.none()

        if self.is_bound:
            # id_tipo = self.data.get('tipo_documento', None)
            try:
                self.fields['tipo_documento'].queryset = TipoDocumento.objects.all()
            except:
                self.fields['tipo_documento'].queryset = TipoDocumento.objects.none()


class FormularioBusquedaRegistro(forms.Form):
    """
    Formulario para la busqueda de registros que se han ingresado en la app
    """

    error_css_class = 'has-error'

    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.all(), label=_("Tipo de Documento"))
    fecha_inicial = forms.DateField(label=_("Fecha Inicial"))
    fecha_final = forms.DateField(label=_("Fecha Final"))
    palabras_claves = forms.CharField(max_length=255, label=_("Palabras Claves"))
    descripcion = forms.CharField(label=_("Descripción"))

    def __init__(self, *args, **kwargs):
        super(FormularioBusquedaRegistro, self).__init__(*args, **kwargs)

        self.fields['tipo_documento'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['fecha_inicial'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_final'].widget.attrs.update({'class': 'form-control'})
        self.fields['palabras_claves'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'rows': '5'})
        self.fields['palabras_claves'].required = False

    def clean_palabras_claves(self):
        data = self.cleaned_data['palabras_claves'].split(',')
        return [PalabraClave.objects.get(nombre__iexact=palabra) for palabra in data if palabra != '']
