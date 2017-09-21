from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import CustomModelForm
from .models import Materia, Modulo, Sesion


class FormularioMateria(CustomModelForm):
    """
    Formulario para crear las Materias.
    """

    class Meta:
        model = Materia
        fields = ('nombre', 'grupos_minimo', 'dependencia', )


class PrioridadMixin:
    OBJETO = _('')

    error_messages = {
        'prioridad_exists': _('Ya existe un %s con esta prioridad.' % OBJETO)
    }


class FormularioModulo(PrioridadMixin, CustomModelForm):
    """
    Formulario para crear los módulos de cada materia.
    """

    OBJETO = _('módulo')

    class Meta:
        model = Modulo
        fields = ('nombre', 'prioridad', 'materia', )

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)

        if 'materia' in cleaned_data and 'prioridad' in cleaned_data:
            if cleaned_data.get('materia').modulos.filter(prioridad=cleaned_data.get('prioridad')).exists():
                self.add_error(
                    'prioridad',
                    forms.ValidationError(self.error_messages['prioridad_exists'], code='prioridad_exists')
                )
        return cleaned_data


class FormularioSesion(PrioridadMixin, CustomModelForm):
    """
    Formulario para crear una sesión.
    """

    OBJETO = _('sesión')

    class Meta:
        model = Sesion
        fields = ('nombre', 'prioridad', 'modulo')


# from django.forms import ModelForm
# from django.db.models import Q
# from academia.models import Reporte, Matricula, Curso, Modulo, Sesion
# from miembros.models import Miembro, CambioTipo


# class FormularioEvaluarModulo(ModelForm):
#     required_css_class = 'requerido'

#     def __init__(self, *args, **kwargs):
#         super(FormularioEvaluarModulo, self).__init__(*args, **kwargs)

#         self.fields['nota'].widget.attrs.update({'class': 'form-control'})

#     class Meta:
#         model = Reporte
#         fields = ('nota', )


# class FormularioPromoverModulo(ModelForm):
#     required_css_class = 'requerido'

#     def __init__(self, est='', *args, **kwargs):
#         super(FormularioPromoverModulo, self).__init__(*args, **kwargs)  # populates the post
#         self.fields['modulo_actual'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

#         if est != '':
#             modEst = est.modulos.all()
#             if est.modulo_actual:
#                 self.fields['modulo_actual'].queryset = est.curso.modulos.exclude(
#                     id__in=modEst).exclude(id__in=[est.modulo_actual.id])
#             else:
#                 self.fields['modulo_actual'].queryset = est.curso.modulos.exclude(id__in=modEst)

#     class Meta:
#         model = Matricula
#         fields = ('modulo_actual',)


# class FormularioCrearCurso(ModelForm):
#     required_css_class = 'requerido'
#     error_css_class = 'has-error'

#     def __init__(self, *args, **kwargs):
#         super(FormularioCrearCurso, self).__init__(*args, **kwargs)  # populates the post
#         self.fields['profesor'].queryset = Miembro.objects.filter(usuario__groups__name__iexact='Maestro')
#         self.fields['estado'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['dia'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['profesor'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['red'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['modulos'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
#         self.fields['material'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Material...'})
#         self.fields['hora'].widget.attrs.update({'class': 'form-control', 'data-mask': '00:00:00'})
#         self.fields['direccion'].widget.attrs.update({'class': 'form-control'})

#     class Meta:
#         model = Curso
#         fields = '__all__'


# class FormularioEditarCurso(ModelForm):
#     required_css_class = 'requerido'
#     error_css_class = 'has-error'

#     def __init__(self, *args, **kwargs):
#         super(FormularioEditarCurso, self).__init__(*args, **kwargs)

#         self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
#         self.fields['estado'].widget.attrs.update({'class': 'form-control'})
#         self.fields['modulos'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['red'].widget.attrs.update({'class': 'form-control'})
#         self.fields['profesor'].widget.attrs.update({'class': 'form-control'})
#         self.fields['material'].widget.attrs.update({'class': 'form-control'})
#         self.fields['dia'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['hora'].widget.attrs.update({'class': 'form-control'})
#         self.fields['direccion'].widget.attrs.update({'class': 'form-control'})

#         self.fields['nombre'].widget.attrs['readonly'] = True
#         self.fields['estado'].widget.attrs['readonly'] = True
#         self.fields['modulos'].widget.attrs['readonly'] = True
#         self.fields['red'].widget.attrs['readonly'] = True
#         self.fields['profesor'].widget.attrs['readonly'] = True
#         self.fields['material'].widget.attrs['readonly'] = True

#     def save(self, commit=True):
#         return super(FormularioEditarCurso, self).save(commit)

#     class Meta:
#         model = Curso
#         # fields = ('direccion', 'dia', 'hora')
#         fields = '__all__'


# class FormularioMatricula(ModelForm):
#     required_css_class = 'requerido'

#     def __init__(self, *args, **kwargs):
#         super(FormularioMatricula, self).__init__(*args, **kwargs)  # populates the post
#         mCurso = Matricula.objects.all().values('estudiante')
#         mLiderMaestro = CambioTipo.objects.filter(
#             Q(nuevoTipo__nombre__iexact='lider') | Q(nuevoTipo__nombre__iexact='maestro')).values('miembro')
#         # mEncuentro = CumplimientoPasos.objects.filter(paso__nombre__iexact='encuentro').values('miembro')
#         # self.fields['estudiante'].queryset = Miembro.objects.filter(
#         #     id__in=mEncuentro).exclude(id__in=mLiderMaestro).exclude(id__in=mCurso).exclude(grupo=None)
#         self.fields['estudiante'].queryset = Miembro.objects.exclude(id__in=mLiderMaestro).exclude(id__in=mCurso).exclude(grupo=None)
#         self.fields['estudiante'].widget.attrs.update(
#             {'class': 'form-control selectpicker', 'data-live-search': 'true'}
#         )
#         self.fields['fecha_inicio'].widget.attrs.update({'class': 'form-control'})

#     class Meta:
#         model = Matricula
#         fields = ('estudiante', 'fecha_inicio')


# class FormularioCrearModulo(ModelForm):
#     required_css_class = 'requerido'

#     def __init__(self, *args, **kwargs):
#         super(FormularioCrearModulo, self).__init__(*args, **kwargs)

#         self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
#         self.fields['porcentaje'].widget.attrs.update({'class': 'form-control'})

#     class Meta:
#         model = Modulo
#         fields = '__all__'


# class FormularioCrearSesion(ModelForm):
#     required_css_class = 'requerido'

#     def __init__(self, *args, **kwargs):
#         super(FormularioCrearSesion, self).__init__(*args, **kwargs)

#         self.fields['nombre'].widget.attrs.update({'class': 'form-control'})

#     class Meta:
#         model = Sesion
#         fields = ('nombre',)


# class FormularioRecibirPago(ModelForm):
#     required_css_class = 'requerido'

#     def __init__(self, *args, **kwargs):
#         super(FormularioRecibirPago, self).__init__(*args, **kwargs)
#         self.fields['pago'].widget.attrs.update({'class': 'form-control'})

#     class Meta:
#         model = Matricula
#         fields = ('pago', )
