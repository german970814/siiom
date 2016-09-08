from treebeard.al_tree import AL_NodeManager


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
