# Django Package
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group, User
from django.db.models.functions import Lower

# Locale Apps
from .models import Area, Departamento, Empleado


class AreaForm(forms.ModelForm):
    """
    Formulario para creación de áreas en SGD
    """
    error_css_class = 'has-error'

    class Meta:
        model = Area
        fields = ['nombre', 'departamento']

    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['departamento'].widget.attrs.update({'class': 'selectpicker'})


class DepartamentoForm(forms.ModelForm):
    """
    Formulario para la creación de departamentos en el SGD
    """
    error_css_class = 'has-error'

    class Meta:
        model = Departamento
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(DepartamentoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})


class EmpleadoForm(forms.ModelForm):
    """
    Formulario para la creacion de empleados en el SGD
    """
    error_css_class = 'has-error'
    correo = forms.EmailField(label=_('Correo Electronico'))
    contrasena = forms.CharField(max_length=255, widget=forms.PasswordInput(), label=_('Contraseña'))
    contrasena_confirmacion = forms.CharField(
        max_length=255, widget=forms.PasswordInput(), label=_('Confirmar Contraseña')
    )
    _accept = [
        'lider', 'administrador', 'maestro', 'pastor', 'agente',
        'miembro', 'coordinador', 'receptor', 'tesorero'
    ]
    tipo_usuario = forms.ModelChoiceField(
        queryset=Group.objects.annotate(nombre=Lower('name')).exclude(nombre__in=_accept),
        label=_('Tipo de Usuario')
    )

    class Meta:
        model = Empleado
        fields = ['areas', 'cedula', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']

    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['correo'].widget.attrs.update({'class': 'form-control'})
        self.fields['contrasena'].widget.attrs.update({'class': 'form-control'})
        self.fields['contrasena_confirmacion'].widget.attrs.update({'class': 'form-control'})
        self.fields['cedula'].widget.attrs.update({'class': 'form-control'})
        self.fields['primer_nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['segundo_nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['primer_apellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['segundo_apellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_usuario'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['areas'].widget.attrs.update({'class': 'selectpicker'})

    def clean(self, *args, **kwargs):
        cleaned_data = super(EmpleadoForm, self).clean(*args, **kwargs)
        usuario_existente = None
        if 'correo' in cleaned_data:
            try:
                usuario_existente = User.objects.get(email=cleaned_data['correo'])
                try:
                    if usuario_existente.empleado:
                        self.add_error('correo', _('Ya existe un empleado con este correo'))
                except Empleado.DoesNotExist:
                    pass

            except User.DoesNotExist:
                pass
        if usuario_existente is None:
            if 'contrasena' in cleaned_data and 'contrasena_confirmacion' in cleaned_data:
                if cleaned_data['contrasena'] != cleaned_data['contrasena_confirmacion']:
                    self.add_error('contrasena', _('Las contraseñas no coinciden'))
                    self.add_error('contrasena_confirmacion', _('Las contraseñas no coinciden'))
