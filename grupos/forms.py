'''
Created on Apr 12, 2011

@author: Migue
'''
from django import forms
from django.db.models import Q
from django.forms.models import ModelForm
from django.contrib.auth.models import Group
from django.db import transaction, IntegrityError
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from grupos.models import Grupo, ReunionGAR, ReunionDiscipulado, Red
from miembros.models import CambioTipo, Miembro
from grupos.models import Predica
from reportes.forms import FormularioRangoFechas
from common.forms import CustomModelForm


class FormularioEditarGrupo(ModelForm):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    class Meta:
        model = Grupo
        fields = ('direccion', 'diaGAR', 'horaGAR')

    def __init__(self, *args, **kwargs):
        super(FormularioEditarGrupo, self).__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['diaGAR'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['horaGAR'].widget.attrs.update({'class': 'form-control', 'data-mask': '00:00'})


class FormularioReportarReunionGrupo(ModelForm):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    class Meta:
        model = ReunionGAR
        exclude = ('grupo', 'confirmacionEntregaOfrenda', 'asistentecia', 'novedades', 'digitada_por_miembro')

    def __init__(self, *args, **kwargs):
        super(FormularioReportarReunionGrupo, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs.update({'class': 'form-control'})
        self.fields['predica'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroTotalAsistentes'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroLideresAsistentes'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroVisitas'].widget.attrs.update({'class': 'form-control'})
        self.fields['ofrenda'].widget.attrs.update({'class': 'form-control'})


class FormularioReportarReunionGrupoAdmin(ModelForm):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    class Meta:
        model = ReunionGAR
        exclude = ('confirmacionEntregaOfrenda', 'asistentecia', 'novedades', 'digitada_por_miembro')

    def __init__(self, *args, **kwargs):
        super(FormularioReportarReunionGrupoAdmin, self).__init__(*args, **kwargs)
        self.fields['grupo'].queryset = Grupo.objects.filter(estado='A').select_related('lider1', 'lider2')
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['fecha'].widget.attrs.update({'class': 'form-control'})
        self.fields['predica'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroTotalAsistentes'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroLideresAsistentes'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroVisitas'].widget.attrs.update({'class': 'form-control'})
        self.fields['ofrenda'].widget.attrs.update({'class': 'form-control'})


class FormularioReportarReunionDiscipulado(ModelForm):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    class Meta:
        model = ReunionDiscipulado
        exclude = ('grupo', 'confirmacionEntregaOfrenda', 'asistentecia')

    def __init__(self, miembro, *args, **kwargs):
        super(FormularioReportarReunionDiscipulado, self).__init__(*args, **kwargs)
        self.fields['predica'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['numeroLideresAsistentes'].widget.attrs.update({'class': 'form-control'})
        self.fields['novedades'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Novedades...'})
        self.fields['ofrenda'].widget.attrs.update({'class': 'form-control'})
        self.fields['predica'].queryset = Predica.objects.filter(miembro__id__in=miembro.pastores())


class FormularioCrearRed(ModelForm):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearRed, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Red
        fields = '__all__'


REUNION_CHOICES = (('1', 'Gar'), ('2', 'Discipulado'))


class FormularioReportesSinEnviar(forms.Form):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    reunion = forms.TypedChoiceField(choices=REUNION_CHOICES, coerce=int, required=True, widget=forms.RadioSelect)
    fechai = forms.DateField(label='Fecha inicial', required=True, widget=forms.DateInput(attrs={'size': 10}))
    fechaf = forms.DateField(label='Fecha final', required=True, widget=forms.DateInput(attrs={'size': 10}))


class FormularioCrearPredica(ModelForm):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        miembro = kwargs.pop('miembro', None)
        super(FormularioCrearPredica, self).__init__(*args, **kwargs)
        print(miembro)
        if miembro is not None:
            if miembro.usuario.has_perm('miembros.es_administrador'):
                print("entre aca")
                grupo_pastor = Group.objects.get(name__iexact='pastor')
                self.fields['miembro'].queryset = Miembro.objects.filter(usuario__groups=grupo_pastor)
            else:
                print("no me fui por aca")
                self.fields['miembro'].queryset = Miembro.objects.filter(id=miembro.id)
                self.fields['miembro'].initial = miembro.id
        else:
            print("error estoy aca")
            self.fields['miembro'].queryset = Miembro.objects.none()
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['miembro'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control',
                                                        'placeholder': 'Descripción...',
                                                        'rows': '3'})

    class Meta:
        model = Predica
        fields = ('miembro', 'descripcion', 'nombre')


class FormularioEditarDiscipulado(ModelForm):
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioEditarDiscipulado, self).__init__(*args, **kwargs)
        self.fields['horaDiscipulado'].widget.attrs.update({'class': 'form-control', 'data-mask': '00:00'})
        self.fields['diaDiscipulado'].widget.attrs.update({'class': 'selectpicker'})

    class Meta:
        model = Grupo
        fields = ('diaDiscipulado', 'horaDiscipulado')


class FormularioTransladarGrupo(forms.Form):
    error_css_class = 'has-error'

    queryset = Grupo.objects.all()
    grupo = forms.ModelChoiceField(queryset=queryset, required=True)

    def __init__(self, red=None, grupo_id=None, *args, **kwargs):
        super(FormularioTransladarGrupo, self).__init__(*args, **kwargs)
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        if red or grupo_id:
            self.fields['grupo'].queryset = self.fields['grupo'].queryset.filter(red=red).exclude(id=grupo_id)


class FormularioReportesEnviados(FormularioRangoFechas):
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.none())  # .filter(estado='A'))

    def __init__(self, *args, **kwargs):
        super(FormularioReportesEnviados, self).__init__(*args, **kwargs)
        self.fields['grupo'].widget.attrs.update(
            {'class': 'selectpicker', 'data-live-search': 'true'}
        )

        if self.is_bound:
            try:
                queryset = Grupo.objects.filter(id=self.data['grupo'])
            except Grupo.DoesNotExist:
                queryset = Grupo.objects.none()

            self.fields['grupo'].queryset = queryset


class FormularioEditarReunionGAR(forms.ModelForm):
    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(FormularioEditarReunionGAR, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        # se comenta la linea que hacia que la fecha no fuera editable
        # self.fields['fecha'].widget.attrs.update({'readonly': ''})

    class Meta:
        model = ReunionGAR
        # exclude = ('grupo', 'asistentecia')
        # se cambia el exclude por fields
        fields = (
            'fecha', 'predica', 'numeroTotalAsistentes',
            'numeroLideresAsistentes', 'numeroVisitas',
            'ofrenda'
        )


class BaseGrupoForm(CustomModelForm):
    """
    Formulario base el manejo de grupo de una iglesia.
    """

    mensaje_error = _lazy('Ha ocurrido un error al guardar el grupo. Por favor intentelo de nuevo.')
    lideres = forms.ModelMultipleChoiceField(queryset=Grupo.objects.none(), label=_lazy('Lideres'))

    class Meta:
        model = Grupo
        fields = [
            'lideres', 'direccion', 'estado', 'fechaApertura', 'diaGAR', 'horaGAR', 'diaDiscipulado',
            'horaDiscipulado', 'nombre', 'barrio'
        ]

    def __init__(self, *args, **kwargs):
        super(BaseGrupoForm, self).__init__(*args, **kwargs)
        self.fields['lideres'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['barrio'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['horaDiscipulado'].widget.attrs.update({'class': 'form-control time-picker'})
        self.fields['horaGAR'].widget.attrs.update({'class': 'form-control time-picker'})
        self.fields['diaDiscipulado'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['fechaApertura'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['estado'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['diaGAR'].widget.attrs.update({'class': 'selectpicker'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})

        self.fields['lideres'].queryset = Miembro.objects.lideres_disponibles()


class GrupoRaizForm(BaseGrupoForm):
    """
    Formulario para la creación o edición del grupo raiz.
    """

    def __init__(self, *args, **kwargs):
        super(GrupoRaizForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['lideres'].queryset = (self.fields['lideres'].queryset | self.instance.lideres.all()).distinct()
            self.fields['lideres'].initial = self.instance.lideres.all()

    def save(self):
        try:
            with transaction.atomic():
                raiz = super(GrupoRaizForm, self).save(commit=False)
                if raiz.pk:
                    raiz.save()
                    raiz.lideres.clear()
                else:
                    raiz = Grupo.add_root(instance=raiz)

                lideres = self.cleaned_data['lideres']
                lideres.update(grupo_lidera=raiz)
                return raiz
        except IntegrityError:
            self.add_error(None, forms.ValidationError(self.mensaje_error))
            return None


class NuevoGrupoForm(BaseGrupoForm):
    """
    Formulario para la creación de un grupo en una iglesia.
    """

    class Meta(BaseGrupoForm.Meta):
        fields = ['parent'] + BaseGrupoForm.Meta.fields

    def __init__(self, red, *args, **kwargs):
        super(NuevoGrupoForm, self).__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        grupos_query = Grupo.objects.prefetch_related('lideres').red(red)
        if grupos_query.count() == 0:
            grupos_query = grupos_query | Grupo.objects.prefetch_related('lideres').filter(id=Grupo.objects.raiz().id)

        self.fields['parent'].queryset = grupos_query
        query_lideres = self.fields['lideres'].queryset.red(red)
        if query_lideres.count() == 0:
            query_lideres = query_lideres | Grupo.objects.raiz().miembro_set.lideres_disponibles()

        self.fields['lideres'].queryset = query_lideres
        self.red = red

    def save(self):
        try:
            with transaction.atomic():
                grupo = super(NuevoGrupoForm, self).save(commit=False)
                grupo.red = self.red

                padre = self.cleaned_data['parent']
                grupo = padre.add_child(instance=grupo)

                lideres = self.cleaned_data['lideres']
                lideres.update(grupo_lidera=grupo, grupo=padre)
                return grupo
        except IntegrityError:
            self.add_error(None, forms.ValidationError(self.mensaje_error))
            return None


class EditarGrupoForm(NuevoGrupoForm):
    """
    Formulario para la edición de un grupo en una iglesia.
    """

    def __init__(self, *args, **kwargs):
        super(EditarGrupoForm, self).__init__(kwargs['instance'].red, *args, **kwargs)
        self.fields['parent'].required = False

        # descendientes = [grupo.id for grupo in Grupo.get_tree(self.instance)]
        # parent_query = self.fields['parent'].queryset.exclude(id__in=descendientes)
        # if self.instance.parent.is_root():
        #     root_query = Grupo.objects.prefetch_related('lideres').filter(id=self.instance.parent.id)
        #     self.fields['parent'].queryset = self.fields['parent'].queryset | root_query

        self.fields['lideres'].queryset = (self.fields['lideres'].queryset | self.instance.lideres.all()).distinct()
        self.fields['lideres'].initial = self.instance.lideres.all()

    def save(self):
        try:
            with transaction.atomic():
                grupo = BaseGrupoForm.save(self)

                # if 'parent' in self.changed_data:
                #     padre = self.cleaned_data['parent']
                #     grupo.move(padre, pos='sorted-child')
                #     self.lideres.all().update(grupo=nuevo_padre)

                if 'lideres' in self.changed_data:
                    grupo.lideres.clear()
                    # padre = self.cleaned_data['parent']
                    lideres = self.cleaned_data['lideres']
                    lideres.update(grupo_lidera=grupo, grupo=self.instance.parent)

                return grupo
        except IntegrityError:
            self.add_error(None, forms.ValidationError(self.mensaje_error))
            return None


class TransladarGrupoForm(forms.Form):
    """
    Formulario para el translado de un grupo. En nuevo se excluyen los descendientes y el mismo.
    """

    error_css_class = 'has-error'
    nuevo = forms.ModelChoiceField(queryset=None)

    def __init__(self, grupo, *args, **kwargs):
        super(TransladarGrupoForm, self).__init__(*args, **kwargs)
        self.fields['nuevo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

        descendientes = [grupo.id for grupo in Grupo.get_tree(grupo)]
        self.fields['nuevo'].queryset = Grupo.objects.exclude(id__in=descendientes).prefetch_related('lideres')

        self.grupo = grupo

    def transladar(self):
        self.grupo.transladar(self.cleaned_data['nuevo'])
