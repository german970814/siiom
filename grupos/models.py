# -*- coding: utf-8 -*-
from django.db import models
from treebeard.al_tree import AL_Node
from miembros.models import CambioTipo


class Red(models.Model):

    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Grupo(AL_Node):
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

    parent = models.ForeignKey('self', related_name='children_set', null=True, db_index=True)
    lider1 = models.ForeignKey('miembros.Miembro', related_name='lider_uno')
    lider2 = models.ForeignKey('miembros.Miembro', null=True, blank=True, related_name='lider_dos')
    direccion = models.CharField(max_length=50)  # poner opcion de asignar la misma del lider por defecto(cual lider?)
    estado = models.CharField(max_length=1, choices=opcionesEstado)
    fechaApertura = models.DateField(verbose_name="Fecha de Apertura")
    diaGAR = models.CharField(max_length=1, choices=opcionesDia, verbose_name='Dia G.A.R')
    horaGAR = models.TimeField(verbose_name='Hora G.A.R')
    diaDiscipulado = models.CharField(
        max_length=1, choices=opcionesDia,
        verbose_name='Dia Discipulado', blank=True, null=True
    )
    horaDiscipulado = models.TimeField(verbose_name='Hora Discipulado', blank=True, null=True)
    nombre = models.CharField(max_length=30)
    red = models.ForeignKey(Red, null=True, blank=True)
    barrio = models.ForeignKey('miembros.Barrio')

    node_order_by = ['id']

    def __str__(self):
        cad = self.lider1.nombre.upper() \
            + " " + self.lider1.primerApellido.upper() + "(" + self.lider1.cedula + ")"

        if self.lider2:
            cad = cad + " - " + self.lider2.nombre.upper() + \
                " " + self.lider2.primerApellido.upper() + "(" + self.lider2.cedula + ")"

        return cad

    @classmethod
    def _obtener_arbol_recursivamente(cls, padre, resultado):
        """Devuelve el arbol de forma recursiva."""

        lista_hijos = []
        for hijo in padre.get_children():
            cls._obtener_arbol_recursivamente(hijo, lista_hijos)

        resultado.append(padre)
        if lista_hijos:
            resultado.append(lista_hijos)

    @classmethod
    def obtener_arbol(cls, padre=None):
        """Devuelve el arbol en una lista de listas incluyendo el padre, que me indica como va el desarrollo de los
        grupos."""

        arbol = []
        if padre is None:
            padre = Grupo.get_root_nodes()[0]

        cls._obtener_arbol_recursivamente(padre, arbol)

        return arbol

    # Deprecado
    @classmethod
    def obterner_arbol_viejo(cls, raiz):
        """Devuelve el arbol en una lista de listas incluyendo el padre, que me indica como va el desarrollo de los
        grupos."""

        pila = [[raiz]]
        act = None
        bajada = True

        discipulos = list(raiz.get_children())
        while len(discipulos) > 0:
            # print 'dis:', discipulos
            hijo = discipulos.pop()
            # print 'd:', d, 'hijo:', hijo
            if hijo:
                if act is not None:
                    pila.append(act)
                sw = True
                while len(pila) > 0 and sw:
                    act = pila.pop()
                    # print 'pila:', pila
                    # print 'act:', act
                    if act[len(act) - 1] == hijo.parent:
                        act.append([hijo])
                        bajada = True
                        sw = False
                    elif act[len(act) - 2] == hijo.parent:
                        act[len(act) - 1].append(hijo)
                        bajada = True
                        sw = False
                    elif isinstance(act[-1], (tuple, list)) and bajada:
                        pila.append(act)
                        pila.append(act[len(act) - 1])
                    elif not isinstance(act[-1], (tuple, list)):
                        bajada = False
                    # print '------------while pila------------'

            if hijo.get_children_count() > 0:
                discipulos.extend(list(hijo.get_children()))
            #  print '----------while disci-----------'
        #  print 'act final:', act
        #  print 'pila final:', pila
        if pila:
            arbol = pila[0]
        else:
            arbol = act

        return arbol

    def listaLideres(self):
        """
        Devuelve una lista con los ids de los lideres del grupo.
        Los lideres estan definidos en los campos lider1, lider2 y sus conyugues
        siempre y cuando estos sean lideres.
        """

        lideres = []
        if self.lider1:
            lideres.append(self.lider1.id)
            if CambioTipo.objects.filter(miembro=self.lider1.conyugue, nuevoTipo__nombre__iexact='lider').exists():
                lideres.append(self.lider1.conyugue.id)
        if self.lider2:
            lideres.append(self.lider2.id)
            if CambioTipo.objects.filter(miembro=self.lider2.conyugue, nuevoTipo__nombre__iexact='lider').exists():
                lideres.append(self.lider2.conyugue.id)
        return lideres

    def miembrosGrupo(self):
        """Devuelve los miembros de un grupo (queryset) sino tiene, devuelve el queryset vacio."""

        lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values('miembro')
        miembros = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='miembro').values('miembro')
        return self.miembro_set.filter(id__in=miembros).exclude(id__in=lideres)


class Predica(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500, blank=True)
    miembro = models.ForeignKey('miembros.Miembro')
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class ReunionGAR(models.Model):
    fecha = models.DateField()
    grupo = models.ForeignKey(Grupo)
    predica = models.CharField(max_length=100, verbose_name='prédica')
    asistentecia = models.ManyToManyField('miembros.Miembro', through='AsistenciaMiembro')
    numeroTotalAsistentes = models.PositiveIntegerField(verbose_name='Número total de asistentes')
    numeroLideresAsistentes = models.PositiveIntegerField(verbose_name='Número de líderes asistentes')
    numeroVisitas = models.PositiveIntegerField(verbose_name='Número de visitas:')
    novedades = models.TextField(max_length=500, default="nada", null=True, blank=True)
    ofrenda = models.DecimalField(max_digits=19, decimal_places=2)
    confirmacionEntregaOfrenda = models.BooleanField(default=False)

    def __str__(self):
        return self.grupo.nombre

    class Meta:
        permissions = (
            ("puede_confirmar_ofrenda_GAR", "puede confirmar la entrega de dinero GAR"),
        )


class AsistenciaMiembro(models.Model):
    miembro = models.ForeignKey('miembros.Miembro')
    reunion = models.ForeignKey(ReunionGAR)
    asistencia = models.BooleanField()

    def __str__(self):
        return self.miembro.nombre + " - " + self.reunion.grupo.nombre


class ReunionDiscipulado(models.Model):
    fecha = models.DateField(auto_now_add=True)
    grupo = models.ForeignKey(Grupo)
    predica = models.ForeignKey(Predica, verbose_name='prédica')
    asistentecia = models.ManyToManyField('miembros.Miembro', through='AsistenciaDiscipulado')
    numeroLideresAsistentes = models.PositiveIntegerField(verbose_name='Número de líderes asistentes')
    novedades = models.TextField(max_length=500)
    ofrenda = models.DecimalField(max_digits=19, decimal_places=2)
    confirmacionEntregaOfrenda = models.BooleanField(default=False)

    def __str__(self):
        return self.grupo.nombre

    class Meta:
        permissions = (
            ("puede_confirmar_ofrenda_discipulado", "puede confirmar la entrega de dinero discipulado"),
        )


class AsistenciaDiscipulado(models.Model):
    miembro = models.ForeignKey('miembros.Miembro')
    reunion = models.ForeignKey(ReunionDiscipulado)
    asistencia = models.BooleanField()

    def __str__(self):
        return self.miembro.nombre + " - " + self.reunion.grupo.nombre
