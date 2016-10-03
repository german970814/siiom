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


class GrupoManager(AL_NodeManager):
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
