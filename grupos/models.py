# -*- coding: utf-8 -*- 
from django.db import models
from Iglesia.miembros.models import Miembro, CambioTipo

class Red(models.Model):

    nombre = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.nombre
    
class Grupo(models.Model):
    opcionesEstado = (
      ('A', 'Activo'),
      ('I', 'Inactivo'),
    )
    opcionesDia = (
      ('0', 'Lunes'),
      ('1', 'Martes'),
      ('2', 'Miercoles'),
      ('3', 'Jueves'),
      ('4', 'Viernes'),
      ('5', 'Sabado'),
      ('6', 'Domingo'),
    )
    
    lider1 = models.ForeignKey('miembros.Miembro', related_name='lider_uno')
    lider2 = models.ForeignKey('miembros.Miembro', null=True, blank= True, related_name='lider_dos')
    direccion = models.CharField(max_length=50)  #poner opcion de asignar la misma del lider por defecto(cual lider?)
    estado = models.CharField(max_length=1, choices=opcionesEstado)
    fechaApertura = models.DateField(verbose_name="Fecha de Apertura")
    diaGAR = models.CharField(max_length=1, choices=opcionesDia, verbose_name = 'Dia G.A.R')
    horaGAR = models.TimeField(verbose_name = 'Hora G.A.R')
    diaDiscipulado = models.CharField(max_length=1, choices=opcionesDia, verbose_name = 'Dia Discipulado')
    horaDiscipulado = models.TimeField(verbose_name = 'Hora Discipulado')
    nombre = models.CharField(max_length=30)
    red = models.ForeignKey(Red, null=True, blank=True)
    barrio = models.ForeignKey('miembros.Barrio')
    
    def __unicode__(self):
        return self.nombre
    
    def listaLideres(self):
        """Devuelve una lista con los ids de los lideres del grupo. Los lideres estan definidos en los campos lider1, lider2 y sus conyugues siempre y cuando estos sean lideres."""
        
        lideres = []
        if self.lider1:
            lideres.append(self.lider1.id)
            if CambioTipo.objects.filter(miembro = self.lider1.conyugue, nuevoTipo__nombre__iexact = 'lider').exists():
                lideres.append(self.lider1.conyugue.id)
        if self.lider2:
            lideres.append(self.lider2.id)
            if CambioTipo.objects.filter(miembro = self.lider2.conyugue, nuevoTipo__nombre__iexact = 'lider').exists():
                lideres.append(self.lider2.conyugue.id)
        return lideres
    
    def miembrosGrupo(self):
        """Devuelve los miembros de un grupo (queryset) sino tiene, devuelve el queryset vacio."""
        
        lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact = 'lider').values('miembro')
        miembros = CambioTipo.objects.filter(nuevoTipo__nombre__iexact = 'miembro').values('miembro')
        return self.miembro_set.filter(id__in = miembros).exclude(id__in = lideres)

class ReunionGAR(models.Model):
    fecha = models.DateField()
    grupo = models.ForeignKey(Grupo)
    predica = models.CharField(max_length=100, verbose_name=u'prédica')
    asistentecia = models.ManyToManyField('miembros.Miembro', through='AsistenciaMiembro')
    numeroLideresAsistentes = models.PositiveIntegerField(verbose_name = u'Número de líderes asistentes')
    numeroVisitas = models.PositiveIntegerField(verbose_name = u'Número de visitas:')
    novedades = models.TextField(max_length=500, default="nada",null= True, blank = True)
    ofrenda = models.PositiveIntegerField()
    confirmacionEntregaOfrenda = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.grupo.nombre
        
    class Meta:
        permissions = (
                        ("puede_confirmar_ofrenda_GAR", "puede confirmar la entrega de dinero GAR"),
                      )    
    
class AsistenciaMiembro(models.Model):
    miembro = models.ForeignKey('miembros.Miembro')
    reunion = models.ForeignKey(ReunionGAR)
    asistencia = models.BooleanField()
    
    def __unicode__(self):
        return self.miembro.nombre + " - " + self.reunion.grupo.nombre
    
class ReunionDiscipulado(models.Model):
    fecha = models.DateField()
    grupo = models.ForeignKey(Grupo)
    predica = models.CharField(max_length=100, verbose_name=u'prédica')
    asistentecia = models.ManyToManyField('miembros.Miembro', through='AsistenciaDiscipulado')
    numeroLideresAsistentes = models.PositiveIntegerField(verbose_name = u'Número de líderes asistentes')
    novedades = models.TextField(max_length=500)
    ofrenda = models.PositiveIntegerField()
    confirmacionEntregaOfrenda = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.grupo.nombre
    
    class Meta:
        permissions = (
            ("puede_confirmar_ofrenda_discipulado", "puede confirmar la entrega de dinero discipulado"),
        )
          
    
class AsistenciaDiscipulado(models.Model):
    miembro = models.ForeignKey('miembros.Miembro')
    reunion = models.ForeignKey(ReunionDiscipulado)
    asistencia = models.BooleanField()
    
    def __unicode__(self):
        return self.miembro.nombre + " - " + self.reunion.grupo.nombre

