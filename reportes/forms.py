# -*- coding: utf-8 -*-

# Django Package
from django import forms
from django.db.models.aggregates import Count
from django.utils.translation import ugettext_lazy as _

# Locale Apps
from grupos.models import Red, Predica, Grupo
from miembros.models import Miembro
from .utils import listaGruposDescendientes_id

__author__ = 'Tania'


MESES_CHOICES = (
    ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
    ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
    ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'),
    ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
)

RED_CHOICES = [(red.id, red.nombre)for red in Red.objects.all()]

REUNION_CHOICES = (('1', 'Gar'), ('2', 'Discipulado'))


class FormularioRangoFechas(forms.Form):
    required_css_class = 'requerido'

    fechai = forms.DateField(label='Fecha inicial', required=True, widget=forms.DateInput(attrs={'size': 10}))
    fechaf = forms.DateField(label='Fecha final', required=True, widget=forms.DateInput(attrs={'size': 10}))

    def __init__(self, *args, **kwargs):
        super(FormularioRangoFechas, self).__init__(*args, **kwargs)
        self.fields['fechai'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/00'})
        self.fields['fechaf'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/00'})


class FormularioVisitasPorMes(forms.Form):
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        super(FormularioVisitasPorMes, self).__init__(*args, **kwargs)
        self.fields['meses'].widget.attrs.update({'id': 'idCheck', 'style': 'list-style:none;'})
        self.fields['ano'].widget.attrs.update({'class': 'form-control', 'data-mask': '0000'})

    ano = forms.CharField(label='año', required=True)
    meses = forms.TypedMultipleChoiceField(
        choices=MESES_CHOICES, coerce=int,
        required=True, widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox m-r-20'}))


class FormularioVisitasRedPorMes(forms.Form):
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        super(FormularioVisitasRedPorMes, self).__init__(*args, **kwargs)
        self.fields['ano'].widget.attrs.update({'class': 'form-control', 'data-mask': '0000'})
        self.fields['red'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

    ano = forms.CharField(label='año', required=True)
    red = forms.ChoiceField(choices=RED_CHOICES)
    meses = forms.TypedMultipleChoiceField(
        choices=MESES_CHOICES, coerce=int,
        required=True, widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox m-r-20'}))


class FormularioReportesSinEnviar(forms.Form):
    required_css_class = 'requerido'
    error_css_class = 'has-error'

    fechai = forms.DateField(label='Fecha inicial', required=True, widget=forms.DateInput(attrs={'size': 10}))
    fechaf = forms.DateField(label='Fecha final', required=True, widget=forms.DateInput(attrs={'size': 10}))
    grupo = forms.ModelChoiceField(label='Grupo', required=True, queryset=Grupo.objects.none())
    descendientes = forms.BooleanField(label='Descendientes', widget=forms.CheckboxInput(), required=False)

    def __init__(self, *args, **kwargs):
        miembro = kwargs.pop('miembro', None)
        grupos = []
        if miembro:
            grupos = listaGruposDescendientes_id(miembro)
        super(FormularioReportesSinEnviar, self).__init__(*args, **kwargs)
        self.fields['fechai'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/00'})
        self.fields['fechaf'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/00'})
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        if miembro and miembro.usuario.has_perm('miembros.es_administrador'):
            self.fields['grupo'].queryset = Grupo.objects.all().select_related('lider1', 'lider2')
        else:
            self.fields['grupo'].queryset = Grupo.objects.filter(
                id__in=grupos
            ).select_related('lider1', 'lider2')


class FormularioPredicas(forms.Form):
    required_css_class = 'requerido'

    predica = forms.ModelChoiceField(queryset=Predica.objects.none(), empty_label=None)

    def __init__(self, miembro, *args, **kwargs):
        super(FormularioPredicas, self).__init__(*args, **kwargs)
        self.fields['predica'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

        if miembro.usuario.has_perm("miembros.es_administrador"):
            self.fields['predica'].queryset = Predica.objects.all()
        else:
            self.fields['predica'].queryset = Predica.objects.filter(miembro__id__in=miembro.pastores())


class FormularioCumplimientoLlamadasLideres(FormularioRangoFechas):
    """Permite escoger entre un rango de fechas y una red."""

    red = forms.ModelChoiceField(queryset=Red.objects.all())

    def __init__(self, *args, **kwargs):
        super(FormularioCumplimientoLlamadasLideres, self).__init__(*args, **kwargs)
        self.fields['red'].widget.attrs.update({'class': 'selectpicker'})

    def obtener_grupos(self):
        fecha_inicial = self.cleaned_data['fechai']
        fecha_final = self.cleaned_data['fechaf']
        red = self.cleaned_data['red']

        grupos = Grupo.objects.filter(red=red, miembro__fechaAsignacionGAR__range=(fecha_inicial, fecha_final))
        grupos = grupos.distinct().annotate(personas_asignadas=Count('miembro'))

        for grupo in grupos:
            grupo.lideres = Miembro.objects.filter(id__in=grupo.listaLideres())
            miembros_asignados = grupo.miembro_set.filter(fechaAsignacionGAR__range=(fecha_inicial, fecha_final))
            grupo.llamadas_realizadas = miembros_asignados.filter(fechaLlamadaLider__isnull=True).count()
            grupo.llamadas_no_realizadas = grupo.personas_asignadas - grupo.llamadas_realizadas

        return grupos


class FormularioEstadisticoReunionesGAR(forms.Form):
    """
    Formulario para los estadisticos de reuniones GAR
    """

    error_css_class = 'has-error'

    grupo = forms.ModelChoiceField(label=_('Grupo'), queryset=Grupo.objects.none())
    fecha_inicial = forms.DateField(label=_('Fecha Inicial'))
    fecha_final = forms.DateField(label=_('Fecha Final'))
    descendientes = forms.BooleanField(label=_('Descendientes'), required=False)
    ofrenda = forms.BooleanField(label=_('Ofrenda'), required=False)
    lideres_asistentes = forms.BooleanField(label=_('Líderes Asistentes'), required=False)
    visitas = forms.BooleanField(label=_('Visitas'), required=False)
    asistentes_regulares = forms.BooleanField(label=_('Asistentes Regulares'), required=False)

    def __init__(self, *args, **kwargs):
        queryset_grupo = kwargs.pop('queryset_grupo', None)
        super(FormularioEstadisticoReunionesGAR, self).__init__(*args, **kwargs)
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})
        self.fields['fecha_inicial'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_final'].widget.attrs.update({'class': 'form-control'})
        if queryset_grupo is not None:
            self.fields['grupo'].queryset = queryset_grupo

    def clean(self, *args, **kwargs):
        cleaned_data = super(FormularioEstadisticoReunionesGAR, self).clean(*args, **kwargs)

        boolean_fields = [
            cleaned_data.get('ofrenda', False),
            cleaned_data.get('lideres_asistentes', False),
            cleaned_data.get('visitas', False),
            cleaned_data.get('asistentes_regulares', False)
        ]

        if all(not x for x in boolean_fields):
            self.add_error('ofrenda', _('Escoge una opción'))
            self.add_error('lideres_asistentes', _('Escoge una opción'))
            self.add_error('visitas', _('Escoge una opción'))
            self.add_error('asistentes_regulares', _('Escoge una opción'))
