import warnings
# Django
from django.db import models
from django.utils.module_loading import import_string

# Third apps
from treebeard.al_tree import AL_NodeManager


class GrupoQuerySet(models.QuerySet):
    """
    Queryset personalizado para los grupos.
    """

    @classmethod
    def get_historial_model(cls):
        """
        :returns:
            Modelo de HistorialEstado.
        """

        return import_string('grupos.models.HistorialEstado')

    def red(self, red):
        """
        :retunrs:
            Un queryset con los grupos filtrados por la red ingresada.

        :param red:
            La red usada para filtrar los grupos.
        """

        return self.filter(red=red)

    def _filter_queryset_by_estado(self, estado):
        """Retorna un queryset de acuerdo al estado en el historial del grupo."""

        return self.annotate(
            latest_historial=models.Max('historiales__id')).filter(
            latest_historial__in=self.get_historial_model().objects.filter(estado=estado)
        )

    def _exclude_queryset_by_estado(self, estado):
        """Retorna un queryset de acuerdo al estado en el historial del grupo."""

        return self.annotate(
            latest_historial=models.Max('historiales__id')
        ).exclude(
            latest_historial__in=self.get_historial_model().objects.filter(estado=estado)
        )

    def activos(self):
        """
        :returns:
            Un queryset con los grupos con estado activo.
        """

        return self._filter_queryset_by_estado(self.get_historial_model().ACTIVO)

    def inactivos(self):
        """
        :returns:
            Un queryset con los grupos con estado inactivo.
        """

        return self._filter_queryset_by_estado(self.get_historial_model().INACTIVO)

    def suspendidos(self):
        """
        :returns:
            Un queryset con los grupos con estado suspendido.
        """

        return self._filter_queryset_by_estado(self.get_historial_model().SUSPENDIDO)

    def archivados(self):
        """
        :returns:
            Un queryset con los grupos con estado archivado.
        """

        return self._filter_queryset_by_estado(self.get_historial_model().ARCHIVADO)

    def _archivados(self):
        """
        :returns:
            Un queryset con los grupos que no tengan estado archivado.
        """

        return self._exclude_queryset_by_estado(self.get_historial_model().ARCHIVADO)

    def _activos(self):
        """
        :returns:
            Un queryset con los grupos que no tengan estado activo.
        """

        return self._exclude_queryset_by_estado(self.get_historial_model().ACTIVO)

    def _inactivos(self):
        """
        :returns:
            Un queryset con los grupos que no tengan estado inactivo.
        """

        return self._exclude_queryset_by_estado(self.get_historial_model().INACTIVO)

    def _suspendidos(self):
        """
        :returns:
            Un queryset con los grupos que no tengan estado suspendido.
        """

        return self._exclude_queryset_by_estado(self.get_historial_model().SUSPENDIDO)


class GrupoManager(AL_NodeManager.from_queryset(GrupoQuerySet)):
    """
    Manager personalizado para los grupos.
    """

    def get_super_queryset(self):
        """
        :returns:
            Retorna el get_queryset() del padre.
        """
        return super().get_queryset()

    def get_queryset(self):
        return self.get_super_queryset()._archivados()  # se excluyen los archivados

    def get(self, *args, **kwargs):
        return self.model._objects.get(*args, **kwargs)

    def archivados(self):
        """
        :returns:
            Un queryset con los grupos que se encuentran en estado archivado.
        """
        return self.model._objects.archivados()

    def raiz(self, iglesia=None):
        """
        :returns:
            La raiz del arbol de grupos de la iglesia ingresada. Si no existe retorna ``None``.

        :param iglesia:
            La iglesia de la cual se va a retornar la raíz.
        """

        if iglesia is not None:
            warnings.warn('Ya no se debe usar el parametro iglesia.')

        nodos = self.model.get_root_nodes()
        if nodos:
            return nodos[0]

        return None

    def sin_confirmar_ofrenda_GAR(self):
        """
        :returns:
            Un queryset con los grupos que tienen pendientes por confirmar la ofrenda de reuniones GAR.
        """

        return self.filter(reuniones_gar__confirmacionEntregaOfrenda=False).distinct()

    def sin_confirmar_ofrenda_discipulado(self):
        """
        :returns:
            Un queryset con los grupos que tienen pendientes por confirmar la ofrenda de reuniones de discipulado.
        """

        return self.filter(reuniones_discipulado__confirmacionEntregaOfrenda=False).distinct()

    def hojas(self, iglesia=None):
        """
        :returns:
            Un QuerySet con los grupos que no tienen descendientes (Incluye los grupos que solo tienen descendientes
            archivados).
        """

        if iglesia is not None:
            warnings.warn('Ya no se debe usar el parametro iglesia en hojas.')
        return self.exclude(children_set__in=self.model.objects.all())


class GrupoManagerStandard(AL_NodeManager.from_queryset(GrupoQuerySet)):
    """Clase de manager para mantener el get_queryset original proveido por django."""
    pass


class HistorialManager(models.Manager):
    """Manager para el modelo de historialestado."""

    def estado(self, estado):
        """
        :returns:
            Un queryset con los historiales filtrados por el estado.

        :param estado:
            El estado a partir del cual se filtraran los historiales.
        """
        return self.filter(estado=estado)
