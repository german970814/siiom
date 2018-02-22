# -*- coding: utf-8 -*-

# Django Package
from django import forms
from django.utils.translation import ugettext_lazy as _

# Locale Apps
from grupos.models import Predica, Grupo, ReunionDiscipulado, AsistenciaDiscipulado
from common.forms import (FormularioRangoFechas as CommonFormFechas, CustomForm)


__author__ = 'Tania'


class FormularioRangoFechas(forms.Form):  # deprecado
    """
    Formulario rango de fechas anterior, se recomienda usar ``common.forms.FormularioRangoFechas``.
    """

    required_css_class = 'requerido'

    fechai = forms.DateField(label='Fecha inicial', widget=forms.DateInput(attrs={'size': 10}))
    fechaf = forms.DateField(label='Fecha final', widget=forms.DateInput(attrs={'size': 10}))

    def __init__(self, *args, **kwargs):
        super(FormularioRangoFechas, self).__init__(*args, **kwargs)
        self.fields['fechai'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/00'})
        self.fields['fechaf'].widget.attrs.update({'class': 'form-control', 'data-mask': '00/00/00'})


class FormularioPredicas(forms.Form):
    """Formulario para ahcer reportes a partir de las predicas."""

    required_css_class = 'requerido'

    predica = forms.ModelChoiceField(queryset=Predica.objects.none(), empty_label=None)

    def __init__(self, miembro, *args, **kwargs):
        super(FormularioPredicas, self).__init__(*args, **kwargs)
        self.fields['predica'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

        if miembro.usuario.has_perm("miembros.es_administrador"):
            self.fields['predica'].queryset = Predica.objects.all()
        else:
            self.fields['predica'].queryset = Predica.objects.filter(miembro__id__in=miembro.pastores())


class FormularioEstadisticoReunionesGAR(forms.Form):
    """
    Formulario para los estadisticos de reuniones GAR.
    """

    error_css_class = 'has-error'

    grupo = forms.ModelChoiceField(label=_('Grupo'), queryset=Grupo.objects.none())
    fecha_inicial = forms.DateField(label=_('Fecha Inicial'))
    fecha_final = forms.DateField(label=_('Fecha Final'))
    descendientes = forms.BooleanField(label=_('Descendientes'), required=False)
    ofrenda = forms.BooleanField(label=_('Ofrenda'), required=False)

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
        return cleaned_data


class FormularioReportesSinConfirmar(CommonFormFechas):
    """
    Formulario para ver los reportes que no se han confirmado de un grupo, de acuerdo a un rango de fechas.
    """
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.prefetch_related('lideres').all().distinct(),
        label=_('grupo')
    )
    descendientes = forms.BooleanField(label=_('Descendientes'), required=False)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['grupo'].widget.attrs.update({
            'class': 'selectpicker',
            'data-live-search': 'true'
        })
        if queryset is not None:
            self.fields['grupo'].queryset = queryset


class TotalizadoReunionDiscipuladoForm(FormularioPredicas, CustomForm):
    """
    Formulario para ver el reporte del totalizado de reuniones de discipulado.
    """

    OFRENDA = 'O'
    ASISTENTES_REGULARES = 'A'
    OPCIONES = (
        (ASISTENTES_REGULARES, _('Número de asistentes regulares')),
        (OFRENDA, _('Ofrenda'))
    )

    grupo_inicial = forms.ModelChoiceField(queryset=Grupo.objects.none(), empty_label=None)
    opcion = forms.ChoiceField(choices=OPCIONES, widget=forms.RadioSelect())

    def __init__(self, miembro, *args, **kwargs):
        super().__init__(miembro, *args, **kwargs)
        self.fields['grupo_inicial'].widget.attrs.update({'class': 'selectpicker', 'data-live-search': 'true'})

        if miembro.usuario.has_perm("miembros.es_administrador"):
            grupo_queryset = Grupo.objects.prefetch_related('lideres', 'historiales').all()
        else:
            grupo_queryset = miembro.grupo_lidera.grupos_red.prefetch_related('lideres', 'historiales')
        self.fields['grupo_inicial'].queryset = grupo_queryset
    
    def obtener_totalizado(self):
        opcion = self.cleaned_data['opcion']
        predica = self.cleaned_data['predica']
        grupo_inicial = self.cleaned_data['grupo_inicial']

        titulo = ''
        tiene_discipulos = False
        discipulos = grupo_inicial.get_children()
        opciones = {'predica': predica.nombre.capitalize(), 'gi': grupo_inicial.nombre.capitalize()}

        n = ['Predica']
        n.extend(discipulos.values_list('nombre', flat=True))
        values = [n]
        l = [predica.nombre.upper()]
        for discipulo in discipulos:
            tiene_discipulos = True
            arbol = Grupo.get_tree(discipulo)

            reuniones = ReunionDiscipulado.objects.filter(predica=predica, grupo__in=arbol)
            if opcion == self.OFRENDA:
                opciones['opt'] = 'Ofrendas'
                titulo = "'Ofrendas'"

                sum_ofrenda = reuniones.aggregate(Sum('ofrenda'))

                if sum_ofrenda['ofrenda__sum'] is None:
                    suma = 0
                else:
                    suma = sum_ofrenda['ofrenda__sum']
                
                l.append(float(suma))
            else: # opcion es asistentes regulares
                opciones['opt'] = 'Asistentes Regulares'
                titulo = "'Asistentes Regulares'"
                numAsis = AsistenciaDiscipulado.objects.filter(reunion__in=reuniones, asistencia=True).count()
                l.append(numAsis)

        values.append(l)
        return opciones, values, titulo, tiene_discipulos

