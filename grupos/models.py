# -*- coding: utf-8 -*-
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _lazy
from treebeard.al_tree import AL_Node
from miembros.models import CambioTipo
from common.models import IglesiaMixin
from consolidacion.utils import clean_direccion
from .managers import GrupoManager


class Red(IglesiaMixin, models.Model):

    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Grupo(IglesiaMixin, AL_Node):
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
        'self', verbose_name=_lazy('grupo origen'), related_name='children_set', null=True, db_index=True
    )
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

    # campos para ubicaciones en mapas
    latitud = models.FloatField(verbose_name='Latitud', blank=True, null=True)
    longitud = models.FloatField(verbose_name='Longitud', blank=True, null=True)

    # managers
    objects = GrupoManager()
    node_order_by = ['id']

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
    def obtener_arbol(cls, padre=None, iglesia=None):
        """
        Devuelve el arbol en una lista de listas incluyendo el padre, que me indica como va el desarrollo de los
        grupos.
        """

        arbol = []
        if padre is None:
            if iglesia is None:
                return []
            else:
                padre = cls.objects.raiz(iglesia)

        if padre is not None:
            cls._obtener_arbol_recursivamente(padre, arbol)

        return arbol

    # Deprecado
    @classmethod
    def obtener_arbol_viejo(cls, raiz=None):  # pragma: no cover
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

    @classmethod
    def obtener_ruta(cls, inicial, final):
        """
        Devuelve una lista con los grupos que conforman la ruta que hay desde el grupo inicial al grupo final
        incluyendo estos grupos.
        """

        ruta = []
        grupo = final

        while grupo != inicial:
            ruta.insert(0, grupo)
            grupo = grupo.get_parent()

        ruta.insert(0, inicial)
        return ruta

    @property
    def discipulos(self):
        """
        Devuelve un queryset con los miembros del grupo que son lideres.
        """

        return self.miembros.lideres2()

    @property
    def reuniones_GAR_sin_ofrenda_confirmada(self):
        """
        Devuelve un queryset con las reuniones GAR que no tienen la ofrenda confirmada.
        """

        return self.reuniones_gar.filter(confirmacionEntregaOfrenda=False)

    @property
    def reuniones_discipulado_sin_ofrenda_confirmada(self):
        """
        Devuelve un queryset con las reuniones de discipulado que no tienen la ofrenda confirmada.
        """

        return self.reuniones_discipulado.filter(confirmacionEntregaOfrenda=False)

    @property
    def grupos_red(self):
        """
        Devuelve un queryset con los grupos de la red del grupo actual. Entiéndase por red los descendientes del grupo
        actual incluyéndose asimismo.
        """

        from .utils import convertir_lista_grupos_a_queryset
        return convertir_lista_grupos_a_queryset(self.get_tree(self))

    @property
    def cabeza_red(self):
        """
        Retorna la cabeza de red del grupo actual.
        """

        ancentros = self.get_ancestors()
        if len(ancentros) > 2:
            return ancentros[2]
        else:
            return None

    @property
    def _estado(self):
        """Retorna el estado del grupo de acuerdo a su historial."""

        return self.historiales.first().estado

    def _get_estado_display(self):
        """Retorna el estado display del grupo de acuerdo a su historial."""

        return self.historiales.first().get_estado_display()

    def confirmar_ofrenda_reuniones_GAR(self, reuniones):
        """
        Confirma la ofrenda de las reuniones GAR ingresadas en la lista. Reuniones es una lista con los ids de las
        reuniones a confirmar.
        """

        self.reuniones_gar.filter(id__in=reuniones).update(confirmacionEntregaOfrenda=True)

    def confirmar_ofrenda_reuniones_discipulado(self, reuniones):
        """
        Confirma la ofrenda de las reuniones de discipulado ingresadas en la lista. Reuniones es una lista con los ids
        de las reuniones a confirmar.
        """

        self.reuniones_discipulado.filter(id__in=reuniones).update(confirmacionEntregaOfrenda=True)

    def trasladar(self, nuevo_padre):
        """
        Traslada el grupo actual y sus descendientes debajo de un nuevo padre en el arbol. A los lideres del grupo
        actual, se les modifica el grupo al que pertenecen, al nuevo grupo padre.
        """

        with transaction.atomic():
            if nuevo_padre != self.parent:
                self.move(nuevo_padre, pos='sorted-child')
                self.lideres.all().update(grupo=nuevo_padre)

                if nuevo_padre.red != self.red:
                    grupos = [grupo.id for grupo in self.get_tree(self)]
                    Grupo.objects.filter(id__in=grupos).update(red=nuevo_padre.red)

    def _trasladar_miembros(self, nuevo_grupo):
        """
        Traslada todos los miembros que no lideran grupo del grupo actual al nuevo grupo.
        """

        self.miembros.filter(grupo_lidera=None).update(grupo=nuevo_grupo)

    def _trasladar_visitas(self, nuevo_grupo):
        """
        Traslada todas las visitas del grupo actual al nuevo grupo.
        """

        self.visitas.update(grupo=nuevo_grupo)

    def _trasladar_encontristas(self, nuevo_grupo):
        """
        Traslada todos los encontristas del grupo actual al nuevo grupo.
        """

        self.encontristas.update(grupo=nuevo_grupo)

    def _trasladar_reuniones_gar(self, nuevo_grupo):
        """
        Traslada todas las reuniones GAR del grupo actual al nuevo grupo.
        """

        self.reuniones_gar.update(grupo=nuevo_grupo)

    def _trasladar_reuniones_discipulado(self, nuevo_grupo):
        """
        Traslada todas las reuniones de discipulado del grupo actual al nuevo grupo.
        """

        self.reuniones_discipulado.update(grupo=nuevo_grupo)

    def fusionar(self, nuevo_grupo):
        """
        Traslada la información asociada al grupo actual (visitas, encontristas, reuniones, miembros, etc) al
        nuevo grupo y elimina el grupo actual.
        """

        if self != nuevo_grupo:
            with transaction.atomic():
                for hijo in self.get_children():
                    hijo.trasladar(nuevo_grupo)

                self._trasladar_visitas(nuevo_grupo)
                self._trasladar_miembros(nuevo_grupo)
                self._trasladar_encontristas(nuevo_grupo)
                self._trasladar_reuniones_gar(nuevo_grupo)
                self._trasladar_reuniones_discipulado(nuevo_grupo)

                self.delete()

    def get_nombre(self):
        # if self.lider2 is not None:
        #     return '{} - {}'.format(self.lider1.primerApellido.upper(), self.lider2.primerApellido.upper())
        # return self.lider1.primerApellido.upper()
        return self.nombre

    def miembrosGrupo(self):
        """Devuelve los miembros de un grupo (queryset) sino tiene, devuelve el queryset vacio."""

        lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values('miembro')
        miembros = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='miembro').values('miembro')
        return self.miembros.filter(id__in=miembros).exclude(id__in=lideres)

    def get_direccion(self):
        """
        Retorna la direccion de manera legible para los buscadores de mapas
        """
        if self.get_position() is None:
            return clean_direccion(self.direccion)
        else:
            return ','.join([str(x) for x in self.get_position()])

    def get_position(self):
        """
        Retorna las coordenadas de un grupo o None
        """
        if self.latitud is not None and self.longitud is not None:
            return [self.latitud, self.longitud]
        return None


class Predica(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500, blank=True)
    miembro = models.ForeignKey('miembros.Miembro')
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class ReunionGAR(models.Model):
    fecha = models.DateField()
    grupo = models.ForeignKey(Grupo, related_name='reuniones_gar')
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
    grupo = models.ForeignKey(Grupo, related_name='reuniones_discipulado')
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


class HistorialEstado(models.Model):
    """Modelo para guardar historial de cambio de estado de los grupos."""

    ACTIVO = 'AC'
    INACTIVO = 'IN'
    SUSPENDIDO = 'SU'
    ARCHIVADO = 'AR'

    OPCIONES_ESTADO = (
        (ACTIVO, 'ACTIVO'),
        (INACTIVO, 'INACTIVO'),
        (SUSPENDIDO, 'SUSPENDIDO'),
        (ARCHIVADO, 'ARCHIVADO'),
    )

    grupo = models.ForeignKey(Grupo, related_name='historiales', verbose_name=_lazy('grupo'))
    fecha = models.DateTimeField(verbose_name=_lazy('fecha'), auto_now_add=True)
    estado = models.CharField(max_length=2, choices=OPCIONES_ESTADO, verbose_name=_lazy('estado'))

    def __str__(self):
        return 'Historial {estado} para grupo: {self.grupo}'.format(self=self, estado=self.get_estado_display())

    class Meta:
        verbose_name = _lazy('Historial')
        verbose_name_plural = _lazy('Historiales')
        ordering = ['-fecha']
