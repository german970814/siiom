# -*- coding: utf-8 -*-
'''
Created on Apr 4, 2011

@author: Migue
'''
from django.forms import ModelForm
from Iglesia.miembros.models import Miembro, Zona, Barrio, CumplimientoPasos,\
    Pasos, Escalafon, CambioEscalafon, TipoMiembro, CambioTipo, DetalleLlamada
from django.db.models import Q
from django import forms
from Iglesia.academia.models import Matricula

class FormularioLiderAgregarMiembro(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self,g='',c=None,*args,**kwargs):
        super (FormularioLiderAgregarMiembro,self ).__init__(*args,**kwargs) # populates the post
        if g != '':
            if g == 'M':
                g = 'F'
            else:
                g = 'M'

            # if c:
            #     self.fields['conyugue'].queryset = Miembro.objects.filter(Q(estadoCivil='S')|Q(estadoCivil='V')| Q(estadoCivil='D')| Q(id=c.id), genero=g)
            # else:
            #     self.fields['conyugue'].queryset = Miembro.objects.filter(Q(estadoCivil='S')|Q(estadoCivil='V')| Q(estadoCivil='D'), genero=g)

    class Meta:
        model = Miembro
        exclude = ('usuario', 'grupo', 'lider', 'pasos', 'escalafon', 'fechaAsignacionGAR',\
                   'asignadoGAR', 'asisteGAR','' 
                   'fechaLlamadaLider', 'detalleLlamadaLider', 'observacionLlamadaLider',\
                   'fechaPrimeraLlamada', 'detallePrimeraLlamada', 'observacionPrimeraLlamada', \
                   'fechaSegundaLlamada', 'detalleSegundaLlamada', 'observacionSegundaLlamada', \
                   'noInteresadoGAR', 'convertido', 'estado', 'conyugue')

class FormularioAdminAgregarMiembro(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self,g='',*args,**kwargs):
        super (FormularioAdminAgregarMiembro,self ).__init__(*args,**kwargs) # populates the post
        if g != '':
            if g == 'M':
                g = 'F'
            else:
                g = 'M'
            self.fields['conyugue'].queryset = Miembro.objects.filter(Q(estadoCivil='S')|Q(estadoCivil='V')| Q(estadoCivil='D'), genero=g)

    class Meta:
        model = Miembro
        exclude = ('usuario', 'grupo', 'lider', 'pasos', 'escalafon', 'fechaAsignacionGAR',\
                   'fechaLlamadaLider', 'detalleLlamadaLider', 'observacionLlamadaLider',\
                   'fechaPrimeraLlamada', 'detallePrimeraLlamada', 'observacionPrimeraLlamada', \
                   'fechaSegundaLlamada', 'detalleSegundaLlamada', 'observacionSegundaLlamada',)
        
class FormularioLlamadaLider(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Miembro
        fields = ('detalleLlamadaLider', 'observacionLlamadaLider')
        
class FormularioPrimeraLlamadaAgente(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Miembro
        fields = ('detallePrimeraLlamada', 'observacionPrimeraLlamada', 'noInteresadoGAR', 'asisteGAR', 'asignadoGAR', 'fechaAsignacionGAR', 'grupo')
        
class FormularioSegundaLlamadaAgente(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Miembro
        fields = ('detalleSegundaLlamada', 'observacionSegundaLlamada', 'asisteGAR', 'noInteresadoGAR')

        
class FormularioCambiarContrasena(forms.Form):
    required_css_class = 'requerido'
    
    contrasenaAnterior = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=20, label=u'Contraseña anterior:')      
    contrasenaNueva = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=20, label=u'Contraseña nueva:')
    contrasenaNuevaVerificacion = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=20, label=u'Verifique contraseña nueva:')

class FormularioAsignarGrupo(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Miembro
        fields = ('grupo', )
        
class FormularioCrearZona(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Zona
        fields = ('nombre', )
        
class FormularioCrearBarrio(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Barrio
        fields = ('nombre', )
        
        
class FormularioPasosMiembro(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = CumplimientoPasos
        fields = ('paso',) 
        
class FormularioCumplimientoPasosMiembro(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, *args, **kwargs):
        super (FormularioCumplimientoPasosMiembro, self ).__init__(*args,**kwargs) # populates the post
        estudiantes = Matricula.objects.all().exclude(estudiante__pasos__nombre__iexact = 'lanzamiento').values('estudiante')
        self.fields['miembro'].queryset = Miembro.objects.filter(id__in = estudiantes)
    
    class Meta:
        model = CumplimientoPasos
        fields = ('miembro', )        
        
class FormularioPasos(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Pasos

class FormularioCrearEscalafon(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Escalafon

class FormularioPromoverEscalafon(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = CambioEscalafon
        fields = ('miembro', 'escalafon')
        
class FormularioCrearTipoMiembro(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = TipoMiembro
        fields = ('nombre', ) 
        
class FormularioCambioTipoMiembro(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, idm = '' ,*args,**kwargs):
        super (FormularioCambioTipoMiembro, self).__init__(*args, **kwargs) # populates the post
        self.idm = idm
        if idm != '':
            m = Miembro.objects.get(id = idm)
            tipos = CambioTipo.objects.filter(miembro = m).values('nuevoTipo')
            self.fields['nuevoTipo'].queryset = TipoMiembro.objects.all().exclude(id__in = tipos)
#            try:
#                mLanzado = CumplimientoPasos.objects.get(miembro = m, paso__nombre__iexact = 'lanzamiento')
#            except:
#                mLanzado = None
#            if mLanzado is None:
#                self.fields['nuevoTipo'].queryset = self.fields['nuevoTipo'].queryset.exclude(nombre__iexact = 'lider')
    
    class Meta:
        model = CambioTipo
        fields = ('nuevoTipo', )
                
class FormularioAsignarUsuario(forms.Form):
    required_css_class = 'requerido'
    
    email = forms.EmailField(label=u'Verificar correo:')      
    contrasena = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=20, label=u'Contraseña:')
    contrasenaVerificacion = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=20, label=u'Verifique contraseña:')


class FormularioDetalleLlamada(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = DetalleLlamada

