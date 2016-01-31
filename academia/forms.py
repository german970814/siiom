'''
Created on 27/04/2011

@author: Conial
'''
from django.forms import ModelForm
from django.db.models import Q
from academia.models import Reporte, Matricula, Curso, Modulo, Sesion
from miembros.models import Miembro, CambioTipo, CumplimientoPasos

class FormularioEvaluarModulo(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Reporte
        fields = ('nota', )
        
class FormularioPromoverModulo(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, est = '', *args, **kwargs):
        super (FormularioPromoverModulo, self ).__init__(*args,**kwargs) # populates the post
        if est != '':
            modEst = est.modulos.all()
            if est.moduloActual:
                self.fields['moduloActual'].queryset = est.curso.modulos.exclude(id__in = modEst).exclude(id__in = [est.moduloActual.id])
            else:
                self.fields['moduloActual'].queryset = est.curso.modulos.exclude(id__in = modEst)
    
    class Meta:
        model = Matricula
        fields = ('moduloActual',)
        
class FormularioCrearCurso(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, *args, **kwargs):
        super (FormularioCrearCurso, self ).__init__(*args,**kwargs) # populates the post
        self.fields['profesor'].queryset = Miembro.objects.filter(usuario__groups__name__iexact = 'Maestro')
    
    class Meta:
        model = Curso

class FormularioEditarCurso(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Curso
        fields = ('direccion', 'dia', 'hora')

class FormularioMatricula(ModelForm):
    required_css_class = 'requerido'
    
    def __init__(self, *args, **kwargs):
        super (FormularioMatricula, self ).__init__(*args,**kwargs) # populates the post
        mCurso = Matricula.objects.all().values('estudiante')
        mLiderMaestro = CambioTipo.objects.filter(Q(nuevoTipo__nombre__iexact = 'lider') | Q(nuevoTipo__nombre__iexact = 'maestro')).values('miembro')
        mEncuentro = CumplimientoPasos.objects.filter(paso__nombre__iexact = 'encuentro').values('miembro')
        self.fields['estudiante'].queryset = Miembro.objects.filter(id__in = mEncuentro).exclude(id__in = mLiderMaestro).exclude(id__in = mCurso).exclude(grupo=None)
    
    class Meta:
        model = Matricula
        fields = ('estudiante', 'fechaInicio')

class FormularioCrearModulo(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Modulo

class FormularioCrearSesion(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Sesion
        fields = ('nombre',)
        
class FormularioRecibirPago(ModelForm):
    required_css_class = 'requerido'
    
    class Meta:
        model = Matricula
        fields = ('pago', )
