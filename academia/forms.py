'''
Created on 27/04/2011

@author: Conial
'''

from django import forms
from django.db.models import Q

from academia.models import Reporte, Matricula, Curso, Modulo, Sesion
from miembros.models import Miembro, CambioTipo, CumplimientoPasos


class FormularioEvaluarModulo(forms.ModelForm):
    """
    Formulario usado para evaluar los modulos de las academias.
    """

    required_css_class = 'requerido'

    class Meta:
        model = Reporte
        fields = ('nota', )

    def __init__(self, *args, **kwargs):
        super(FormularioEvaluarModulo, self).__init__(*args, **kwargs)
        self.fields['nota'].widget.attrs.update({'class': 'form-control'})


class FormularioPromoverModulo(forms.ModelForm):
    """
    Formulario usado para promover modulos de acuerdo a la matricula.
    """

    required_css_class = 'requerido'

    class Meta:
        model = Matricula
        fields = ('moduloActual', )

    def __init__(self, est='', *args, **kwargs):
        super(FormularioPromoverModulo, self).__init__(*args, **kwargs)
        self.fields['moduloActual'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

        if est != '':
            modEst = est.modulos.all()
            if est.moduloActual:
                self.fields['moduloActual'].queryset = est.curso.modulos.exclude(
                    id__in=modEst).exclude(id__in=[est.moduloActual.id])
            else:
                self.fields['moduloActual'].queryset = est.curso.modulos.exclude(id__in=modEst)


class FormularioCrearCurso(forms.ModelForm):
    """Formulario para crear los cursos."""

    required_css_class = 'requerido'
    error_css_class = 'has-error'

    class Meta:
        model = Curso
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearCurso, self).__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Miembro.objects.filter(usuario__groups__name__iexact='Maestro')
        self.fields['estado'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['dia'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['profesor'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['red'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['modulos'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['material'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Material...'})
        self.fields['hora'].widget.attrs.update({'class': 'form-control', 'data-mask': '00:00:00'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})


class FormularioEditarCurso(forms.ModelForm):
    """
    Formulario para editar los cursos de academia creados.
    """

    required_css_class = 'requerido'
    error_css_class = 'has-error'

    class Meta:
        model = Curso
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormularioEditarCurso, self).__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['estado'].widget.attrs.update({'class': 'form-control'})
        self.fields['modulos'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['red'].widget.attrs.update({'class': 'form-control'})
        self.fields['profesor'].widget.attrs.update({'class': 'form-control'})
        self.fields['material'].widget.attrs.update({'class': 'form-control'})
        self.fields['dia'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['hora'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})

        self.fields['nombre'].widget.attrs['readonly'] = True
        self.fields['estado'].widget.attrs['readonly'] = True
        self.fields['modulos'].widget.attrs['readonly'] = True
        self.fields['red'].widget.attrs['readonly'] = True
        self.fields['profesor'].widget.attrs['readonly'] = True
        self.fields['material'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        return super(FormularioEditarCurso, self).save(commit)


class FormularioMatricula(forms.ModelForm):
    """
    Formulario para crear las matriculas a la academia de acuerdo a un miembro.
    """

    required_css_class = 'requerido'

    class Meta:
        model = Matricula
        fields = ('estudiante', 'fechaInicio')

    def __init__(self, *args, **kwargs):
        super(FormularioMatricula, self).__init__(*args, **kwargs)
        mCurso = Matricula.objects.all().values('estudiante')
        mLiderMaestro = CambioTipo.objects.filter(
            Q(nuevoTipo__nombre__iexact='lider') | Q(nuevoTipo__nombre__iexact='maestro')).values('miembro')
        mEncuentro = CumplimientoPasos.objects.filter(paso__nombre__iexact='encuentro').values('miembro')
        self.fields['estudiante'].queryset = Miembro.objects.filter(
            id__in=mEncuentro).exclude(id__in=mLiderMaestro).exclude(id__in=mCurso).exclude(grupo=None)
        self.fields['estudiante'].widget.attrs.update(
            {'class': 'form-control selectpicker', 'data-live-search': 'true'}
        )
        self.fields['fechaInicio'].widget.attrs.update({'class': 'form-control'})


class FormularioCrearModulo(forms.ModelForm):
    """Formulario para crear modulos."""

    required_css_class = 'requerido'

    class Meta:
        model = Modulo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearModulo, self).__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['porcentaje'].widget.attrs.update({'class': 'form-control'})


class FormularioCrearSesion(forms.ModelForm):
    """
    Formulario para crear sesiones de modulos en las academias.
    """

    required_css_class = 'requerido'

    class Meta:
        model = Sesion
        fields = ('nombre',)

    def __init__(self, *args, **kwargs):
        super(FormularioCrearSesion, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})


class FormularioRecibirPago(forms.ModelForm):
    """Formulario para recibir los pagos que se hacen en la academia."""

    required_css_class = 'requerido'

    class Meta:
        model = Matricula
        fields = ('pago', )

    def __init__(self, *args, **kwargs):
        super(FormularioRecibirPago, self).__init__(*args, **kwargs)
        self.fields['pago'].widget.attrs.update({'class': 'form-control'})
