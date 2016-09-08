from grupos.models import Grupo
from .base import GruposBaseTest


class GrupoModelTest(GruposBaseTest):
    """
    Pruebas unitarias para el modelo Grupo.
    """

    def test_obtener_arbol_no_hay_raiz_devuelve_lista_vacio(self):
        """
        Prueba que si no existe raiz en el arbol de grupos, devuelva una lista vacía.
        """

        Grupo.objects.all().delete()
        lista_obtenida = Grupo.obtener_arbol()
        self.assertListEqual(lista_obtenida, [])

    def test_obtener_arbol_completo(self):
        """
        Prueba que la lista obtenida sea igual a la lista del arbol completo.
        """

        lista_obtenida = Grupo.obtener_arbol()
        self.assertListEqual(lista_obtenida, self.lista_arbol_completo)

    def test_obtener_arbol_padre_especifico(self):
        """
        Prueba que la lista obtenida sea igual a la lista del arbol de un padre especifico.
        """

        cb2 = Grupo.objects.get(id=3)
        lista_obtenida = Grupo.obtener_arbol(cb2)
        self.assertListEqual(lista_obtenida, self.lista_arbol_cb2)
