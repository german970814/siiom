from django.db import models
from treebeard.al_tree import AL_NodeManager
from common.managers import IglesiaMixinQuerySet


class GrupoQuerySet(IglesiaMixinQuerySet, models.QuerySet):
    """
    Queryset personalizado para los grupos.
    """

    def red(self, red):
        """
        Devuelve un queryset con los grupos filtrados por la red ingresada.
        """

        return self.filter(red=red)

    def get_historial_model(self):
        """Retorna el modelo de Historialestado."""

        if not hasattr(self, 'historial_model'):
            # self.historial_model = [x for x in filter(
            #     lambda relation: relation.related_model._meta.model_name == 'historialestado',
            #     self.model._meta.related_objects
            # )][0].related_model
            self.historial_model = self.model._meta.get_field('historiales').related_model
        return self.historial_model

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
        """Devuelve un queryset con los grupos con estado activo."""

        return self._filter_queryset_by_estado(self.get_historial_model().ACTIVO)

    def inactivos(self):
        """Devuelve un queryset con los grupos en estado inactivo."""

        return self._filter_queryset_by_estado(self.get_historial_model().INACTIVO)

    def suspendidos(self):
        """Devuelve un queryset con los grupos en estado suspendido."""

        return self._filter_queryset_by_estado(self.get_historial_model().SUSPENDIDO)

    def archivados(self):
        """Devuelve un queryset con los grupos en estado archivado."""

        return self._filter_queryset_by_estado(self.get_historial_model().ARCHIVADO)

    def _archivados(self):
        """Retorna un queryset con todos los grupos a excepcion de los que se encuentran archivados."""

        return self._exclude_queryset_by_estado(self.get_historial_model().ARCHIVADO)

    def _activos(self):
        """Retorna un queryset con todos los grupos a excepcion de los que se encuentran activos."""

        return self._exclude_queryset_by_estado(self.get_historial_model().ACTIVO)

    def _inactivos(self):
        """Retorna un queryset con todos los grupos a excepcion de los que se encuentran inactivos."""

        return self._exclude_queryset_by_estado(self.get_historial_model().INACTIVO)

    def _suspendidos(self):
        """Retorna un queryset con todos los grupos a excepcion de los que se encuentran suspendidos."""

        return self._exclude_queryset_by_estado(self.get_historial_model().SUSPENDIDO)


class GrupoManager(AL_NodeManager.from_queryset(GrupoQuerySet)):
    """
    Manager personalizado para los grupos.
    """

    def get_super_queryset(self):
        """Retorna el get_queryset original de la clase."""
        return super().get_queryset()

    def get_queryset(self):
        return self.get_super_queryset()._archivados()  # se excluyen los archivados

    def get(self, *args, **kwargs):
        return self.model._objects.get(*args, **kwargs)

    def archivados(self):
        # raise NotImplementedError('Debes asegugarte de usar "Grupo._objects.archivados()"')
        return self.model._objects.archivados()

    def raiz(self, iglesia):
        """
        Devuelve la raiz del arbol de grupos de la iglesia ingresada. Si no existe retorna None.
        """

        nodos = self.model.get_root_nodes().iglesia(iglesia)
        if nodos:
            return nodos[0]

        return None

    def sin_confirmar_ofrenda_GAR(self):
        """
        Devuelve un queryset con los grupos que tienen pendientes por confirmar la ofrenda de reuniones GAR.
        """

        return self.filter(reuniones_gar__confirmacionEntregaOfrenda=False).distinct()

    def sin_confirmar_ofrenda_discipulado(self):
        """
        Devuelve un queryset con los grupos que tienen pendientes por confirmar la ofrenda de reuniones de discipulado.
        """

        return self.filter(reuniones_discipulado__confirmacionEntregaOfrenda=False).distinct()


class GrupoManagerStandard(AL_NodeManager.from_queryset(GrupoQuerySet)):
    """Clase de manager para mantener el get_queryset original proveido por django."""
    pass


class HistorialManager(models.Manager):
    """Manager para el modelo de historialestado."""

    def estado(self, estado):
        return self.filter(estado=estado)
