'''
Created on Apr 12, 2011

@author: Migue
'''
from django import forms
from django.db.models import Q
from django.forms.models import ModelForm
from Iglesia.grupos.models import Grupo, ReunionGAR, ReunionDiscipulado, Red
from Iglesia.miembros.models import CambioTipo, Miembro
from grupos.models import Predica


class FormularioEditarGrupo(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:        
        model = Grupo
        fields = ('direccion', \
                  'diaGAR', 'horaGAR')
    def __init__(self, *args, **kwargs):
        super(FormularioEditarGrupo, self).__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['diaGAR'].widget.attrs.update({'class' : 'form-control'}) 
        self.fields['horaGAR'].widget.attrs.update({'class' : 'form-control'})      
        
class FormularioReportarReunionGrupo(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = ReunionGAR
        exclude = ('grupo', 'confirmacionEntregaOfrenda', 'asistentecia', 'novedades')

    def __init__(self, *args, **kwargs):
        super(FormularioReportarReunionGrupo, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.attrs.update({'class' : 'form-control'})
        self.fields['predica'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['numeroTotalAsistentes'].widget.attrs.update({'class' : 'form-control'})
        self.fields['numeroLideresAsistentes'].widget.attrs.update({'class' : 'form-control'})
        self.fields['numeroVisitas'].widget.attrs.update({'class' : 'form-control'})
        self.fields['ofrenda'].widget.attrs.update({'class' : 'form-control'})

class FormularioReportarReunionGrupoAdmin(ModelForm):
    required_css_class = 'requerido'

    class Meta:
        model = ReunionGAR
        exclude = ('confirmacionEntregaOfrenda', 'asistentecia', 'novedades')

    def __init__(self, *args, **kwargs):
        super(FormularioReportarReunionGrupoAdmin, self).__init__(*args, **kwargs)
        self.fields['grupo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['fecha'].widget.attrs.update({'class' : 'form-control'})
        self.fields['predica'].widget.attrs.update({'class' : 'form-control'})
        self.fields['numeroTotalAsistentes'].widget.attrs.update({'class' : 'form-control'})
        self.fields['numeroLideresAsistentes'].widget.attrs.update({'class' : 'form-control'})
        self.fields['numeroVisitas'].widget.attrs.update({'class' : 'form-control'})
        self.fields['ofrenda'].widget.attrs.update({'class' : 'form-control'})
        
class FormularioReportarReunionDiscipulado(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = ReunionDiscipulado
        exclude = ('grupo', 'confirmacionEntregaOfrenda', 'asistentecia')

    def __init__(self, miembro, *args, **kwargs):
        super(FormularioReportarReunionDiscipulado, self).__init__(*args, **kwargs)
        self.fields['predica'].widget.attrs.update({'class' : 'form-control'})   
        self.fields['numeroLideresAsistentes'].widget.attrs.update({'class' : 'form-control'}) 
        self.fields['novedades'].widget.attrs.update({'class' : 'form-control'})
        self.fields['ofrenda'].widget.attrs.update({'class' : 'form-control'})
        self.fields['predica'].queryset = Predica.objects.filter(miembro__id__in = miembro.pastores())
        
class FormularioCrearRed(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Red
        
class FormularioCrearGrupo(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, red = '', new=True, *args, **kwargs):
        super (FormularioCrearGrupo,self ).__init__(*args, **kwargs) # populates the post
        if red != '':
            lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact = 'lider').values('miembro')
            grupos = Grupo.objects.all()
            lidGrupos = []
            for g in grupos:
                lidGrupos.extend(g.listaLideres())
            if new:
                query1 = Miembro.objects.filter(id__in = lideres).filter(Q(grupo__red = red) | Q(grupo__red = None)).exclude(id__in = lidGrupos)
                query2 = Miembro.objects.filter(id__in = lideres).filter(Q(grupo__red = red) | Q(grupo__red = None)).exclude(id__in = lidGrupos)
            else:
                lider1 = self.instance.lider1.id
                lidGrupos.remove(lider1)
                query1 = Miembro.objects.filter(id__in = lideres).filter(Q(grupo__red = red) | Q(grupo__red = None)).exclude(id__in = lidGrupos)
                lidGrupos.append(lider1)
                if self.instance.lider2 is not None:
                    lider2 = self.instance.lider2.id
                    lidGrupos.remove(lider2)
                query2 = Miembro.objects.filter(id__in = lideres).filter(Q(grupo__red = red) | Q(grupo__red = None)).exclude(id__in = lidGrupos)
            self.fields['lider1'].queryset = query1
            self.fields['lider2'].queryset = query2
    
    class Meta:
        model = Grupo
        exclude = ('red',)

class FormularioCrearGrupoRaiz(ModelForm):
    required_css_class = 'requerido'

    def __init__(self, new=True, *args, **kwargs):
        super (FormularioCrearGrupoRaiz,self ).__init__(*args, **kwargs) # populates the post
        lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact = 'lider').values('miembro')
        grupos = Grupo.objects.all()
        lidGrupos = []
        for g in grupos:
            lidGrupos.extend(g.listaLideres())
        if new:
            query1 = Miembro.objects.filter(id__in = lideres).exclude(id__in = lidGrupos)
            query2 = Miembro.objects.filter(id__in = lideres).exclude(id__in = lidGrupos)
        else:
            lider1 = self.instance.lider1.id
            lidGrupos.remove(lider1)
            query1 = Miembro.objects.filter(id__in = lideres).exclude(id__in = lidGrupos)
            lidGrupos.append(lider1)
            if self.instance.lider2 is not None:
                lider2 = self.instance.lider2.id
                lidGrupos.remove(lider2)
            query2 = Miembro.objects.filter(id__in = lideres).exclude(id__in = lidGrupos)
        self.fields['lider1'].queryset = query1
        self.fields['lider2'].queryset = query2

    class Meta:
        model = Grupo
        exclude = ('red',)

REUNION_CHOICES = (('1', 'Gar'), ('2', 'Discipulado'))

class FormularioReportesSinEnviar(forms.Form):
    required_css_class = 'requerido'
    
    reunion = forms.TypedChoiceField(choices = REUNION_CHOICES, coerce = int, required = True, widget = forms.RadioSelect)
    fechai = forms.DateField(label = 'Fecha inicial', required = True, widget = forms.DateInput(attrs = {'size' : 10}))
    fechaf = forms.DateField(label = 'Fecha final', required = True, widget = forms.DateInput(attrs = {'size' : 10}))

class FormularioCrearPredica(ModelForm):
    required_css_class = 'requerido'

    class Meta:
        model = Predica
        exclude = ('miembro',)
