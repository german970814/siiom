# Django Package
from django.utils.translation import ugettext as _
from django import forms

# Locale Apps
from .models import Requisicion, DetalleRequisicion, Adjunto, Historial


class FormularioSolicitudRequisicion(forms.ModelForm):
    """
    Formulario para la creacion de solicitudes de requisición
    """
    error_css_class = 'has-error'

    class Meta:
        model = Requisicion
        fields = ('observaciones', 'prioridad')

    def __init__(self, *args, **kwargs):
        super(FormularioSolicitudRequisicion, self).__init__(*args, **kwargs)
        self.fields['observaciones'].widget.attrs.update({'class': 'form-control'})
        self.fields['prioridad'].widget.attrs.update({'class': 'selectpicker'})


class FormularioDetalleRequisicion(forms.ModelForm):
    """
    Formulario para la creacion de los detalles de la solicitud de requisicion
    """
    error_css_class = 'has-error'

    class Meta:
        model = DetalleRequisicion
        fields = (
            'cantidad', 'descripcion', 'referencia',
            'marca', 'valor_aprobado', 'total_aprobado', 'forma_pago'
        )

    def __init__(self, *args, **kwargs):
        super(FormularioDetalleRequisicion, self).__init__(*args, **kwargs)
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'rows': '2'})
        self.fields['referencia'].widget.attrs.update({'class': 'form-control'})
        self.fields['marca'].widget.attrs.update({'class': 'form-control'})
        self.fields['valor_aprobado'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_aprobado'].widget.attrs.update({'class': 'form-control'})
        self.fields['forma_pago'].widget.attrs.update({'class': 'form-control'})


class FormularioAdjunto(forms.ModelForm):
    """
    Formulario para la creacion de archivos adjuntos de las requisiciones
    """
    error_css_class = 'has-error'

    class Meta:
        model = Adjunto
        fields = ('archivo', )

    def __init__(self, *args, **kwargs):
        super(FormularioAdjunto, self).__init__(*args, **kwargs)


class FormularioRequisicionesJefe(forms.Form):
    """
    Formulario para las requisiciones que puede aprobar el jefe
    """

    error_css_class = 'has-error'

    id_requisicion = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(FormularioRequisicionesJefe, self).__init__(*args, **kwargs)

        self.fields['id_requisicion'].widget = forms.HiddenInput()


class FormularioRequisicionesCompras(forms.Form):
    """
    Formulario para las requisiciones que pueden ver los usuarios de compras
    """

    error_css_class = 'has-error'

    id_requisicion = forms.IntegerField()

    observacion = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(FormularioRequisicionesCompras, self).__init__(*args, **kwargs)
        self.fields['observacion'].widget.attrs.update({'class': 'form-control'})
        self.fields['id_requisicion'].widget = forms.HiddenInput()

    def clean(self, *args, **kwargs):
        cleaned_data = super(FormularioRequisicionesCompras, self).clean(*args, **kwargs)
        if 'id_requisicion' in cleaned_data and 'observacion' in cleaned_data:
            if 'rechazar' in self.data and cleaned_data['observacion'] == '':
                self.add_error('observacion', _("Este campo debe ser obligatorio"))


class FormularioObservacionHistorial(forms.ModelForm):
    """
    Formulario para la creaciond de observaciones de el historial de una requisicion
    """

    error_css_class = 'has-error'

    class Meta:
        model = Historial
        fields = ('observacion', )

    def __init__(self, *args, **kwargs):
        super(FormularioObservacionHistorial, self).__init__(*args, **kwargs)
        self.fields['observacion'].widget.attrs.update({'class': 'form-control'})

        if self.initial and 'observacion' in self.initial:
            self.fields['observacion'].widget.attrs.update({'readonly': ''})
