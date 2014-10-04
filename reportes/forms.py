# -*- coding: utf-8 -*-

from django import forms
from grupos.models import Red
from miembros.models import Miembro

__author__ = 'Tania'

class FormularioRangoFechas(forms.Form):
    required_css_class = 'requerido'

    fechai = forms.DateField(label='Fecha inicial', required=True)
    fechaf = forms.DateField(label='Fecha final', required=True)

    def __init__(self, *args, **kwargs):
        super(FormularioRangoFechas, self).__init__(*args, **kwargs)
        self.fields['fechai'].widget.attrs.update({'class' : 'form-control'})
        self.fields['fechaf'].widget.attrs.update({'class' : 'form-control'})       

MESES_CHOICES = (('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), \
    ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre'))

class FormularioVisitasPorMes(forms.Form):
    required_css_class = 'requerido'

    ano = forms.CharField(label=u'año', required=True)
    meses = forms.TypedMultipleChoiceField(choices=MESES_CHOICES, coerce=int, required=True, widget=forms.CheckboxSelectMultiple(attrs={'class':'check_meses'}))

RED_CHOICES = [(red.id, red.nombre)for red in Red.objects.all()]

class FormularioVisitasRedPorMes(forms.Form):
    required_css_class = 'requerido'

    ano = forms.CharField(label=u'año', required=True)
    red = forms.ChoiceField(choices=RED_CHOICES)
    meses = forms.TypedMultipleChoiceField(choices=MESES_CHOICES, coerce=int, required=True, widget=forms.CheckboxSelectMultiple(attrs={'class':'check_meses'}))

REUNION_CHOICES = (('1', 'Gar'), ('2', 'Discipulado'))

class FormularioReportesSinEnviar(forms.Form):
    required_css_class = 'requerido'

    reunion = forms.TypedChoiceField(choices = REUNION_CHOICES, coerce = int, required = True, widget = forms.RadioSelect)
    fechai = forms.DateField(label = 'Fecha inicial', required = True, widget = forms.DateInput(attrs = {'size' : 10}))
    fechaf = forms.DateField(label = 'Fecha final', required = True, widget = forms.DateInput(attrs = {'size' : 10}))

    def __init__(self, *args, **kwargs):
        super(FormularioReportesSinEnviar, self).__init__(*args, **kwargs)
        self.fields['fechai'].widget.attrs.update({'class' : 'form-control'})
        self.fields['fechaf'].widget.attrs.update({'class' : 'form-control'})         
