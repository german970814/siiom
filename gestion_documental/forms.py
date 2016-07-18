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

    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.none(), label=_("Tipo de Documento"))
    fecha_inicial = forms.DateField(label=_("Fecha Inicial"))
    fecha_final = forms.DateField(label=_("Fecha Final"))
    palabras_claves = forms.CharField(max_length=255, label=_("Palabras Claves"))
    descripcion = forms.CharField(label=_("Descripción"), required=False)
    area = forms.ModelChoiceField(queryset=Area.objects.none(), label=_("Área"))

    def __init__(self, *args, **kwargs):
        empleado = kwargs.pop('empleado')
        super(FormularioBusquedaRegistro, self).__init__(*args, **kwargs)

        self.fields['tipo_documento'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['fecha_inicial'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_final'].widget.attrs.update({'class': 'form-control'})
        self.fields['palabras_claves'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'rows': '5'})
        self.fields['palabras_claves'].required = False
        self.fields['area'].widget.attrs.update({'class': 'selectpicker'})

        if empleado:
            if empleado.usuario.has_perm('organizacional.es_administrador_sgd'):
                self.fields['area'].queryset = Area.objects.all()
            else:
                self.fields['area'].queryset = empleado.areas.all()

        if self.is_bound:
            area_id = self.data.get('area', None)
            if area_id:
                area = Area.objects.get(id=area_id)
                try:
                    query_tipo_documento = TipoDocumento.objects.filter(areas=area)
                    self.fields['tipo_documento'].queryset = query_tipo_documento
                except Area.DoesNotExist:
                    self.fields['tipo_documento'].queryset = TipoDocumento.objects.none()

    def clean_palabras_claves(self):
        data = self.cleaned_data['palabras_claves'].split(',')
        return [PalabraClave.objects.get(nombre__iexact=palabra) for palabra in data if palabra != '']


class TipoDocumentoForm(forms.ModelForm):
    """
    Formulario para la creacion de tipos de documentos en SGD
    """
    error_css_class = 'has-error'

    class Meta:
        model = TipoDocumento
        fields = ['nombre', 'areas']

    def __init__(self, *args, **kwargs):
        super(TipoDocumentoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['areas'].widget.attrs.update({'class': 'selectpicker'})


class PalabraClaveForm(forms.ModelForm):
    """
    Formulario para la creacion de tipos de documentos en SGD
    """
    error_css_class = 'has-error'

    class Meta:
        model = PalabraClave
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(PalabraClaveForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})


class FormularioComentario(forms.Form):
    """
    Formulario de creacion de comentarios
    """
    error_css_class = 'has-error'

    comentario = forms.CharField(label=_('Comentario'), required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(FormularioComentario, self).__init__(*args, **kwargs)
        self.fields['comentario'].widget.attrs.update({'class': 'form-control', 'rows': '4', 'cols': '50'})
