from django import forms
from .models import Requisicion, DetalleRequisicion, Adjunto


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
