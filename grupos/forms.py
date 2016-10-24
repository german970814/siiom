'''
Created on Apr 12, 2011

@author: Migue
'''

# Django
from django import forms
from django.db.models import Q
from django.forms.models import ModelForm
from django.contrib.auth.models import Group
from django.db import transaction, IntegrityError
from django.utils.translation import ugettext as _, ugettext_lazy as _lazy
from django.core.exceptions import ValidationError

# Apps
from grupos.models import Grupo, ReunionGAR, ReunionDiscipulado, Red
from miembros.models import CambioTipo, Miembro
from grupos.models import Predica
from reportes.forms import FormularioRangoFechas
from common.forms import CustomModelForm


class FormularioReunionGARBase(forms.ModelForm):
    """
    Formulario base de validaciones para las reuniones GAR
    """
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    no_realizo_grupo = forms.BooleanField(label=_('No se realizo Realizó Grupo'), required=False)

    class Meta:
        model = ReunionGAR
        fields = (
            'fecha', 'predica', 'ofrenda',
            'numeroTotalAsistentes', 'numeroVisitas', 'numeroLideresAsistentes'
        )

    def __init__(self, *args, **kwargs):
        super(FormularioReunionGARBase, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs.update({'class': 'form-control'})
        self.fields['predica'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroTotalAsistentes'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroLideresAsistentes'].widget.attrs.update({'class': 'form-control'})
        self.fields['numeroVisitas'].widget.attrs.update({'class': 'form-control'})
        self.fields['ofrenda'].widget.attrs.update({'class': 'form-control'})
        self.fields['predica'].required = False

    def clean(self, *args, **kwargs):
        cleaned_data = super(FormularioReunionGARBase, self).clean(*args, **kwargs)

        numero_lideres = cleaned_data.get('numeroLideresAsistentes', None)
        numero_asistentes = cleaned_data.get('numeroTotalAsistentes', None)
        numero_visitas = cleaned_data.get('numeroVisitas', None)
        no_realizo_grupo = cleaned_data.get('no_realizo_grupo', False)
        predica = cleaned_data.get('predica', None)

        if not no_realizo_grupo:
            if predica is None or predica == '':
                self.add_error('predica', _('Este campo es obligatorio.'))

            if numero_asistentes == 0:
                self.add_error(
                    'numeroTotalAsistentes',
                    _('Numero Total de asistentes no puede ser igual a 0, o escoja la opción de "NO Realicé Grupo"')
                )

        if numero_asistentes is not None and numero_lideres is not None and numero_visitas is not None:
            if numero_lideres > 0:
                if numero_lideres > numero_asistentes:
                    self.add_error(
                        'numeroLideresAsistentes', _('Número de Líderes NO puede ser mayor a Número Total de Asistentes')
                    )
            if numero_visitas > 0:
                if numero_visitas >= numero_asistentes:
                    self.add_error(
                        'numeroVisitas', _('Número Visitas NO puede ser mayor o igual a Número Total de Asistentes')
                    )
            if numero_visitas + numero_lideres > numero_asistentes:
                self.add_error(
                    'numeroVisitas',
                    _('Asegurate que la suma de los líderes y las visitas no sea mayor a el total de asistentes')
                )
                self.add_error(
                    'numeroLideresAsistentes',
                    _('Asegurate que la suma de los líderes y las visitas no sea mayor a el total de asistentes')
                )
        else:
            raise ValidationError(_('Asegurate de Haber llenado todos los campos'))

        return cleaned_data


class FormularioEditarGrupo(forms.ModelForm):
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


class FormularioReportarReunionGrupo(FormularioReunionGARBase):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    class Meta(FormularioReunionGARBase.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super(FormularioReportarReunionGrupo, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        super(FormularioReportarReunionGrupo, self).clean(*args, **kwargs)


class FormularioReportarReunionGrupoAdmin(FormularioReunionGARBase):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    class Meta(FormularioReunionGARBase.Meta):
        fields = ('grupo', ) + FormularioReunionGARBase.Meta.fields

    def __init__(self, *args, **kwargs):
        super(FormularioReportarReunionGrupoAdmin, self).__init__(*args, **kwargs)
        self.fields['grupo'].queryset = Grupo.objects.prefetch_related('lideres').filter(estado=Grupo.ACTIVO)
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})


class FormularioReportarReunionDiscipulado(forms.ModelForm):
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


class FormularioCrearRed(forms.ModelForm):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearRed, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Red
        fields = '__all__'


# <<<<<<< HEAD
# =======
# class FormularioCrearGrupo(forms.ModelForm):
#     error_css_class = 'has-error'
#     required_css_class = 'requerido'
#
#     def __init__(self, *args, **kwargs):
#         red = kwargs.pop('red', None)
#         new = kwargs.pop('new', None)
#         super(FormularioCrearGrupo, self).__init__(*args, **kwargs)
#         self.fields['lider1'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['lider2'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['estado'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['diaGAR'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['diaDiscipulado'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['barrio'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['horaGAR'].widget.attrs.update({'class': 'form-control', 'data-mask': '00:00:00'})
#         self.fields['fechaApertura'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/0000'})
#         self.fields['horaDiscipulado'].widget.attrs.update({'class': 'form-control', 'data-mask': '00:00:00'})
#         self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
#         self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
#
#         if red:
#             lideres = CambioTipo.objects.filter(
#                 nuevoTipo__nombre__iexact='lider',
#                 miembro__grupo__red=red
#             ).select_related('miembro').values_list('miembro', flat=True)
#             lideres_exclude = []
#             query = Miembro.objects.filter(id__in=lideres).select_related('conyugue')
#             # Block QuerySet que demora
#             for lider in query:
#                 if lider.grupoLidera():
#                     lideres_exclude.append(lider.id)
#             query = query.exclude(id__in=lideres_exclude)
#             # endblock
#
#             self.fields['lider1'].queryset = query
#             self.fields['lider2'].queryset = query  # query2
#
#         if not new:
#             query_lider1 = self.fields['lider1'].queryset | Miembro.objects.filter(id=self.instance.lider1.id)
#             self.fields['lider1'].queryset = query_lider1
#
#             if self.instance.lider2:
#                 query_lider2 = self.fields['lider2'].queryset | Miembro.objects.filter(id=self.instance.lider2.id)
#                 self.fields['lider2'].queryset = query_lider2
#
#         # if red != '':
#         #     lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values('miembro')
#         #     grupos = Grupo.objects.all().select_related('lider1', 'lider2')
#         #     lidGrupos = []
#         #     for g in grupos:
#         #         lidGrupos.extend(g.listaLideres())
#         #     if new:
#         #         query1 = Miembro.objects.filter(
#         #             id__in=lideres).filter(Q(grupo__red=red) | Q(grupo__red=None)).exclude(id__in=lidGrupos)
#         #         query2 = Miembro.objects.filter(
#         #             id__in=lideres).filter(Q(grupo__red=red) | Q(grupo__red=None)).exclude(id__in=lidGrupos)
#         #     else:
#         #         lider1 = self.instance.lider1.id
#         #         lidGrupos.remove(lider1)
#         #         query1 = Miembro.objects.filter(
#         #             id__in=lideres).filter(Q(grupo__red=red) | Q(grupo__red=None)).exclude(id__in=lidGrupos)
#         #         lidGrupos.append(lider1)
#         #         if self.instance.lider2 is not None:
#         #             lider2 = self.instance.lider2.id
#         #             lidGrupos.remove(lider2)
#         #         query2 = Miembro.objects.filter(
#         #             id__in=lideres).filter(Q(grupo__red=red) | Q(grupo__red=None)).exclude(id__in=lidGrupos)
#
#     def clean(self, *args, **kwargs):
#         cleaned_data = super(FormularioCrearGrupo, self).clean(*args, **kwargs)
#
#         if 'lider1' in cleaned_data and 'lider2' in cleaned_data:
#             if cleaned_data['lider1'] == cleaned_data['lider2']:
#                 self.add_error('lider1', 'Lider1 no puede ser igual a lider2')
#                 self.add_error('lider2', 'Lider2 no puede ser igual a lider1')
#
#     class Meta:
#         model = Grupo
#         exclude = ('red',)
#
#
# class FormularioCrearGrupoRaiz(forms.ModelForm):
#     error_css_class = 'has-error'
#     required_css_class = 'requerido'
#
#     def __init__(self, new=True, *args, **kwargs):
#         super(FormularioCrearGrupoRaiz, self).__init__(*args, **kwargs)
#         lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values('miembro')
#         grupos = Grupo.objects.all()
#         lidGrupos = []
#         for g in grupos:
#             lidGrupos.extend(g.listaLideres())
#         if new:
#             query1 = Miembro.objects.filter(id__in=lideres).exclude(id__in=lidGrupos)
#             query2 = Miembro.objects.filter(id__in=lideres).exclude(id__in=lidGrupos)
#         else:
#             lider1 = self.instance.lider1.id
#             lidGrupos.remove(lider1)
#             query1 = Miembro.objects.filter(id__in=lideres).exclude(id__in=lidGrupos)
#             lidGrupos.append(lider1)
#             if self.instance.lider2 is not None:
#                 lider2 = self.instance.lider2.id
#                 lidGrupos.remove(lider2)
#             query2 = Miembro.objects.filter(id__in=lideres).exclude(id__in=lidGrupos)
#         self.fields['lider1'].queryset = query1 | Miembro.objects.filter(id__in=self.instance.listaLideres())
#         self.fields['lider2'].queryset = query2 | Miembro.objects.filter(id__in=self.instance.listaLideres())
#         self.fields['lider1'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['lider2'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['barrio'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
#         self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
#         self.fields['horaGAR'].widget.attrs.update({'class': 'form-control time-picker'})
#         self.fields['horaGAR'].required = False
#         self.fields['diaDiscipulado'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['diaDiscipulado'].required = False
#         self.fields['fechaApertura'].widget.attrs.update({'class': 'form-control'})
#         self.fields['estado'].widget.attrs.update({'class': 'form-control'})
#         self.fields['diaGAR'].widget.attrs.update({'class': 'selectpicker'})
#         self.fields['horaDiscipulado'].widget.attrs.update({'class': 'form-control time-picker'})
#         self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
#
#     class Meta:
#         model = Grupo
#         exclude = ('red',)
#
# >>>>>>> master
REUNION_CHOICES = (('1', 'Gar'), ('2', 'Discipulado'))


class FormularioReportesSinEnviar(forms.Form):
    error_css_class = 'has-error'
    required_css_class = 'requerido'

    reunion = forms.TypedChoiceField(choices=REUNION_CHOICES, coerce=int, required=True, widget=forms.RadioSelect)
    fechai = forms.DateField(label='Fecha inicial', required=True, widget=forms.DateInput(attrs={'size': 10}))
    fechaf = forms.DateField(label='Fecha final', required=True, widget=forms.DateInput(attrs={'size': 10}))


class FormularioCrearPredica(forms.ModelForm):
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


class FormularioEditarDiscipulado(forms.ModelForm):
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


class FormularioEditarReunionGAR(FormularioReunionGARBase):

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
        super().__init__(*args, **kwargs)
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
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['lideres'].queryset = (self.fields['lideres'].queryset | self.instance.lideres.all()).distinct()
            self.fields['lideres'].initial = self.instance.lideres.all()

    def save(self):
        try:
            with transaction.atomic():
                raiz = super().save(commit=False)
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
        super().__init__(*args, **kwargs)
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
                grupo = super().save(commit=False)
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
        super().__init__(kwargs['instance'].red, *args, **kwargs)
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
        super().__init__(*args, **kwargs)
        self.fields['nuevo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

        descendientes = [grupo.id for grupo in Grupo.get_tree(grupo)]
        self.fields['nuevo'].queryset = Grupo.objects.exclude(id__in=descendientes).prefetch_related('lideres')

        self.grupo = grupo

    def transladar(self):
        self.grupo.transladar(self.cleaned_data['nuevo'])
