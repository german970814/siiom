from django.db import models
from treebeard.al_tree import AL_NodeManager


class GrupoQuerySet(models.QuerySet):
    """
    Queryset personalizado para los grupos.
    """

    def red(self, red):
        """
        Devuelve un queryset con los grupos filtrados por la red ingresada.
        """

        return self.filter(red=red)

    def activos(self, **kwargs):
        """
        Devuelve un queryset con los grupos con estado activo.
        """
        return self.filter(estado=self.model.ACTIVO, **kwargs)


class GrupoManager(AL_NodeManager.from_queryset(GrupoQuerySet)):
    """
    Manager personalizado para los grupos.
    """

    def raiz(self):
        """
        Devuelve la raiz del arbol de grupos. Si no existe retorna None.
        """

        nodos = self.model.get_root_nodes()
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
