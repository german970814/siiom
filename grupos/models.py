# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _lazy
from treebeard.al_tree import AL_Node
from miembros.models import CambioTipo
from .managers import GrupoManager, GrupoQuerySet


class Red(models.Model):

    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Grupo(AL_Node):
    """
    Modelo para guardar la información de los grupos de la iglesia.
    """

    # opciones
    ACTIVO = 'A'
    INACTIVO = 'I'
    ESTADOS = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )

    LUNES = '0'
    MARTES = '1'
    MIERCOLES = '2'
    JUEVES = '3'
    VIERNES = '4'
    SABADO = '5'
    DOMINGO = '6'
    DIAS_SEMANA = (
        (LUNES, 'Lunes'),
        (MARTES, 'Martes'),
        (MIERCOLES, 'Miercoles'),
        (JUEVES, 'Jueves'),
        (VIERNES, 'Viernes'),
        (SABADO, 'Sabado'),
        (DOMINGO, 'Domingo'),
    )

    parent = models.ForeignKey(
        'self', verbose_name=_lazy('padre'), related_name='children_set', null=True, db_index=True
    )
    lider1 = models.ForeignKey('miembros.Miembro', related_name='lider_uno', null=True, blank=True)
    lider2 = models.ForeignKey('miembros.Miembro', null=True, blank=True, related_name='lider_dos')
    # poner opcion de asignar la misma del lider por defecto(cual lider?)
    direccion = models.CharField(verbose_name=_lazy('dirección'), max_length=50)
    estado = models.CharField(verbose_name=_lazy('estado'), max_length=1, choices=ESTADOS)
    fechaApertura = models.DateField(verbose_name=_lazy("fecha de apertura"))
    diaGAR = models.CharField(verbose_name=_lazy('dia G.A.R'), max_length=1, choices=DIAS_SEMANA)
    horaGAR = models.TimeField(verbose_name=_lazy('hora G.A.R'))
    diaDiscipulado = models.CharField(
        verbose_name=_lazy('dia discipulado'), max_length=1, choices=DIAS_SEMANA, blank=True, null=True
    )
    horaDiscipulado = models.TimeField(verbose_name=_lazy('hora discipulado'), blank=True, null=True)
    nombre = models.CharField(verbose_name=_lazy('nombre'), max_length=30)
    red = models.ForeignKey(Red, verbose_name=('red'), null=True, blank=True)
    barrio = models.ForeignKey('miembros.Barrio', verbose_name=_lazy('barrio'))

    node_order_by = ['id']

    # managers
    objects = GrupoManager.from_queryset(GrupoQuerySet)()

    class Meta:
        verbose_name = _lazy('grupo')
        verbose_name_plural = _lazy('grupos')

    def __str__(self):
        lideres = ["{0} {1}({2})".format(
            lider.nombre.upper(), lider.primerApellido.upper(), lider.cedula
        ) for lider in self.lideres.all()]

        return " - ".join(lideres)

    @classmethod
    def _obtener_arbol_recursivamente(cls, padre, resultado):
        """
        Devuelve el arbol de forma recursiva.
        """

        lista_hijos = []
        for hijo in padre.get_children().prefetch_related('lideres'):
            cls._obtener_arbol_recursivamente(hijo, lista_hijos)

        resultado.append(padre)
        if lista_hijos:
            resultado.append(lista_hijos)

    @classmethod
    def obtener_arbol(cls, padre=None):
        """
        Devuelve el arbol en una lista de listas incluyendo el padre, que me indica como va el desarrollo de los
        grupos.
        """

        arbol = []
        if padre is None:
            padre = cls.objects.raiz()

        if padre is not None:
            cls._obtener_arbol_recursivamente(padre, arbol)

        return arbol

    # Deprecado
    @classmethod
    def obtener_arbol_viejo(cls, raiz=None):
        """
        Devuelve el arbol en una lista de listas incluyendo el padre, que me indica como va el desarrollo de los
        grupos.
        """

        arbol = []
        if raiz is None:
            raiz = cls.objects.raiz()

        if raiz is not None:
            pila = [[raiz]]
            act = None
            bajada = True

            discipulos = list(raiz.get_children().select_related('parent').prefetch_related('lideres'))
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
                hijos = hijo.get_children().select_related('parent').prefetch_related('lideres')
                if len(hijos) > 0:
                    discipulos.extend(list(hijos))
                #  print '----------while disci-----------'
            #  print 'act final:', act
            #  print 'pila final:', pila
            if pila:
                arbol = pila[0]
            else:
                arbol = act

        return arbol

    @property
    def discipulos(self):
        """
        Devuelve un queryset con los miembros del grupo que son lideres.
        """

        return self.miembro_set.lideres2()

    @property
    def reuniones_GAR_sin_ofrenda_confirmada(self):
        """
        Devuelve un queryset con las reuniones GAR que no tienen la ofrenda confirmada.
        """

        return self.reuniongar_set.filter(confirmacionEntregaOfrenda=False)

    @property
    def reuniones_discipulado_sin_ofrenda_confirmada(self):
        """
        Devuelve un queryset con las reuniones de discipulado que no tienen la ofrenda confirmada.
        """

        return self.reuniondiscipulado_set.filter(confirmacionEntregaOfrenda=False)

    def confirmar_ofrenda_reuniones_GAR(self, reuniones):
        """
        Confirma la ofrenda de las reuniones GAR ingresadas en la lista. Reuniones es una lista con los ids de las
        reuniones a confirmar.
        """

        self.reuniongar_set.filter(id__in=reuniones).update(confirmacionEntregaOfrenda=True)

    def confirmar_ofrenda_reuniones_discipulado(self, reuniones):
        """
        Confirma la ofrenda de las reuniones de discipulado ingresadas en la lista. Reuniones es una lista con los ids
        de las reuniones a confirmar.
        """

        self.reuniondiscipulado_set.filter(id__in=reuniones).update(confirmacionEntregaOfrenda=True)

    def transladar(self, nuevo_padre):
        """
        Translada el grupo actual y sus descendientes debajo de un nuevo padre en el arbol. A los lideres del grupo
        actual, se les modifica el grupo al que pertenecen, al nuevo grupo padre.
        """

        with transaction.atomic():
            if nuevo_padre != self.parent:
                self.move(nuevo_padre, pos='sorted-child')
                self.lideres.all().update(grupo=nuevo_padre)

                if nuevo_padre.red != self.red:
                    grupos = [grupo.id for grupo in self.get_tree(self)]
                    Grupo.objects.filter(id__in=grupos).update(red=nuevo_padre.red)

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
    digitada_por_miembro = models.BooleanField(default=True)

    def __str__(self):
        return self.grupo.nombre

    class Meta:
        permissions = (
            ("puede_confirmar_ofrenda_GAR", "puede confirmar la entrega de dinero GAR"),
        )

    @property
    def realizada(self):
        """
        Retorna True si la ReunionGAR fue realizada, de lo contrario retorna False
        """
        if self.numeroLideresAsistentes > 0:
            return True
        else:
            if self.numeroTotalAsistentes > 0:
                return True
        return False


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
