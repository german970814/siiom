# -*- coding: utf-8 -*-

from django import forms
from django.db.models.aggregates import Count
from grupos.models import Red, Predica, Grupo
from miembros.models import Miembro

__author__ = 'Tania'

class FormularioRangoFechas(forms.Form):
    required_css_class = 'requerido'

    fechai = forms.DateField(label='Fecha inicial', required=True, widget = forms.DateInput(attrs = {'size' : 10}))
    fechaf = forms.DateField(label='Fecha final', required=True, widget = forms.DateInput(attrs = {'size' : 10}))

    def __init__(self, *args, **kwargs):
        super(FormularioRangoFechas, self).__init__(*args, **kwargs)
        self.fields['fechai'].widget.attrs.update({'class':'form-control','data-mask':'00/00/00'})
        self.fields['fechaf'].widget.attrs.update({'class' : 'form-control','data-mask':'00/00/00'})       

MESES_CHOICES = (('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), \
    ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'))

class FormularioVisitasPorMes(forms.Form):
    required_css_class = 'requerido'

    def __init__(self,*args,**kwargs):
        super(FormularioVisitasPorMes,self).__init__(*args,**kwargs)

        self.fields['meses'].widget.attrs.update({'id':'idCheck','style':'list-style:none;'})
        self.fields['ano'].widget.attrs.update({'class':'form-control','data-mask':'0000'})

    ano = forms.CharField(label='año', required=True)
    meses = forms.TypedMultipleChoiceField(choices=MESES_CHOICES, coerce=int, required=True, widget=forms.CheckboxSelectMultiple(attrs={'class':'checkbox m-r-20'}))

RED_CHOICES = [(red.id, red.nombre)for red in Red.objects.all()]

class FormularioVisitasRedPorMes(forms.Form):
    required_css_class = 'requerido'

    def __init__(self,*args,**kwargs):
        super(FormularioVisitasRedPorMes,self).__init__(*args,**kwargs)

        self.fields['ano'].widget.attrs.update({'class':'form-control','data-mask':'0000'})

    ano = forms.CharField(label='año', required=True)
    red = forms.ChoiceField(choices=RED_CHOICES)
    meses = forms.TypedMultipleChoiceField(choices=MESES_CHOICES, coerce=int, required=True, widget=forms.CheckboxSelectMultiple(attrs={'class':'checkbox m-r-20'}))

REUNION_CHOICES = (('1', 'Gar'), ('2', 'Discipulado'))


class FormularioReportesSinEnviar(forms.Form):
    required_css_class = 'requerido'

    fechai = forms.DateField(label='Fecha inicial', required=True, widget=forms.DateInput(attrs={'size': 10}))
    fechaf = forms.DateField(label='Fecha final', required=True, widget=forms.DateInput(attrs={'size': 10}))

    def __init__(self, *args, **kwargs):
        super(FormularioReportesSinEnviar, self).__init__(*args, **kwargs)
        self.fields['fechai'].widget.attrs.update({'class' : 'form-control'})
        self.fields['fechaf'].widget.attrs.update({'class' : 'form-control'})         

class FormularioPredicas(forms.Form):
    required_css_class = 'requerido'

    predica = forms.ModelChoiceField(queryset=Predica.objects.none(), empty_label=None)

    def __init__(self, miembro, *args, **kwargs):
        super(FormularioPredicas, self).__init__(*args, **kwargs)
        self.fields['predica'].widget.attrs.update({'class':'selectpicker','data-live-search':'true'})

        if miembro.usuario.has_perm("miembros.es_administrador"):
            self.fields['predica'].queryset = Predica.objects.all()
        else:
            self.fields['predica'].queryset = Predica.objects.filter(miembro__id__in = miembro.pastores())


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
