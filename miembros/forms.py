# -*- coding: utf-8 -*-
'''
Created on Apr 4, 2011

@author: Migue
'''
from django.forms import ModelForm
from miembros.models import Miembro, Zona, Barrio, CumplimientoPasos,\
    Pasos, Escalafon, CambioEscalafon, TipoMiembro, CambioTipo, DetalleLlamada
from django.db.models import Q
from django import forms
from academia.models import Matricula

class FormularioLiderAgregarMiembro(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self,g='',c=None,*args,**kwargs):
        super (FormularioLiderAgregarMiembro,self ).__init__(*args,**kwargs) # populates the post
        if g != '':
            if g == 'M':
                g = 'F'
            else:
                g = 'M'

        self.fields['nombre'].widget.attrs.update({'class':'form-control'})
        self.fields['primerApellido'].widget.attrs.update({'class':'form-control'})
        self.fields['segundoApellido'].widget.attrs.update({'class':'form-control'})
        self.fields['telefono'].widget.attrs.update({'class':'form-control'})
        self.fields['celular'].widget.attrs.update({'class':'form-control'})
        self.fields['direccion'].widget.attrs.update({'class':'form-control'})
        self.fields['fechaNacimiento'].widget.attrs.update({'class':'form-control'})
        self.fields['cedula'].widget.attrs.update({'class':'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['estadoCivil'].widget.attrs.update({'class':'form-control'})
        self.fields['profesion'].widget.attrs.update({'class':'form-control'})
        self.fields['barrio'].widget.attrs.update({'class':'form-control'})
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
        self.fields['barrio'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Miembro
        exclude = ('usuario', 'grupo', 'lider', 'pasos', 'escalafon', 'fechaAsignacionGAR',\
                   'fechaLlamadaLider', 'detalleLlamadaLider', 'observacionLlamadaLider',\
                   'fechaPrimeraLlamada', 'detallePrimeraLlamada', 'observacionPrimeraLlamada', \
                   'fechaSegundaLlamada', 'detalleSegundaLlamada', 'observacionSegundaLlamada',)
        
class FormularioLlamadaLider(ModelForm):
    required_css_class = 'requerido'

    def __init__(self,*args,**kwargs):
        super(FormularioLlamadaLider,self).__init__(*args,**kwargs)

        self.fields['detalleLlamadaLider'].widget.attrs.update({'class':'form-control'})
        self.fields['observacionLlamadaLider'].widget.attrs.update({'class':'form-control'})
    
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
    
    contrasenaAnterior = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=20, label='Contraseña anterior:')
    contrasenaNueva = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=20, label='Contraseña nueva:')
    contrasenaNuevaVerificacion = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=20, label='Verifique contraseña nueva:')

class FormularioAsignarGrupo(ModelForm):
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        super(FormularioAsignarGrupo,self).__init__(*args,**kwargs)
        self.fields['grupo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search' : 'true'})
    
    class Meta:
        model = Miembro
        fields = ('grupo',)
        
class FormularioCrearZona(ModelForm):
    required_css_class = 'requerido'
    def __init__(self, *args, **kwargs):
        super(FormularioCrearZona,self).__init__(*args,**kwargs)

        self.fields['nombre'].widget.attrs.update({'class':'form-control'})
    
    class Meta:
        model = Zona
        fields = ('nombre', )
        
class FormularioCrearBarrio(ModelForm):
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        super(FormularioCrearBarrio, self).__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class':'form-control'})
    
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
        self.fields['miembro'].widget.attrs.update({'class':'selectpicker','data-live-search':'true'})
    
    class Meta:
        model = CumplimientoPasos
        fields = ('miembro', )        
        
class FormularioPasos(ModelForm):
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        super (FormularioPasos, self ).__init__(*args,**kwargs)
        
        self.fields['nombre'].widget.attrs.update({'class':'form-control'})
        self.fields['prioridad'].widget.attrs.update({'class':'form-control'})
    
    class Meta:
        model = Pasos
        fields = '__all__'

class FormularioCrearEscalafon(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, *args, **kwargs):
        super(FormularioCrearEscalafon,self).__init__(*args,**kwargs)

        self.fields['celulas'].widget.attrs.update({'class':'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class':'form-control', 'placeholder':'Descripción...'})
        self.fields['logro'].widget.attrs.update({'class':'form-control','placeholder':'Logros...'})
        self.fields['rango'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Escalafon
        fields = '__all__'

class FormularioPromoverEscalafon(ModelForm):
    required_css_class = 'requerido'

    def __init__(self, *args, **kwargs):
        super(FormularioPromoverEscalafon, self).__init__(*args, **kwargs)
        self.fields['miembro'].widget.attrs.update({'class':'selectpicker','data-live-search':'true'})
        self.fields['escalafon'].widget.attrs.update({'class':'selectpicker'})
    
    class Meta:
        model = CambioEscalafon
        fields = ('miembro', 'escalafon')
        
class FormularioCrearTipoMiembro(ModelForm):
    required_css_class = 'requerido'
    def __init__(self, *args, **kwargs):
        super (FormularioCrearTipoMiembro, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = TipoMiembro
        fields = ('nombre', ) 
        
class FormularioCambioTipoMiembro(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, idm = '' ,*args,**kwargs):
        super (FormularioCambioTipoMiembro, self).__init__(*args, **kwargs) # populates the post
        self.fields['nuevoTipo'].widget.attrs.update({'class': 'selectpicker', 'data-live-search' : 'true'})
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
    
    email = forms.EmailField(label='Verificar correo:')
    contrasena = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=20, label='Contraseña:')
    contrasenaVerificacion = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=20, label='Verifique contraseña:')


class FormularioDetalleLlamada(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, *args, **kwargs):
        super (FormularioDetalleLlamada, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = DetalleLlamada
        fields = '__all__'


class FormularioRecuperarContrasenia(forms.Form):
    required_css_class = 'requerido'
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(FormularioRecuperarContrasenia, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class':'form-control'})