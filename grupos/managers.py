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

    def _get_historial_model(self):
        """Retorna el modelo de Historialestado."""

        Historial = [x for x in filter(
            lambda relation: relation.related_model._meta.model_name == 'historialestado',
            self.model._meta.related_objects
        )][0].related_model

        return Historial

    def _get_queryset_by_estado(self, estado):
        """Retorna un queryset de acuerdo al estado en el historial del grupo."""

        return self.annotate(
            latest_historial=models.Max('historiales__id')).filter(
            historiales__id=models.F('latest_historial'), historiales__estado=estado
        )

    def activos(self, **kwargs):
        """Devuelve un queryset con los grupos con estado activo."""

        model = self._get_historial_model()
        return self._get_queryset_by_estado(model.ACTIVO)

    def inactivos(self, **kwargs):
        """Devuelve un queryset con los grupos en estado inactivo."""

        model = self._get_historial_model()
        return self._get_queryset_by_estado(model.INACTIVO)


class GrupoManager(AL_NodeManager.from_queryset(GrupoQuerySet)):
    """
    Manager personalizado para los grupos.
    """

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

        return self.filter(reuniongar__confirmacionEntregaOfrenda=False).distinct()

    def sin_confirmar_ofrenda_discipulado(self):
        """
        Devuelve un queryset con los grupos que tienen pendientes por confirmar la ofrenda de reuniones de discipulado.
        """

        return self.filter(reuniondiscipulado__confirmacionEntregaOfrenda=False).distinct()
