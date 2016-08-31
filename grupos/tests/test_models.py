from django.test import TestCase
from grupos.models import Grupo
from .base import GruposBaseTest


class GrupoModelTest(GruposBaseTest):
    """
    Prueba el modelo Grupo.
    """

    def test_obtener_raiz_arbol(self):
        """Grupo obtenido sea la raiz del arbol."""

        raiz = Grupo.obtener_raiz()
        padre = Grupo.objects.get(id=1)
        self.assertEqual(raiz, padre)

    def test_obtener_arbol_completo(self):
        """Lista obtenida sea igual a la lista del arbol completo."""

        lista_obtenida = Grupo.obtener_arbol()
        self.assertListEqual(lista_obtenida, self.lista_arbol_completo)

    def test_obtener_arbol_padre_especifico(self):
        """Lista obtenida sea igual a la lista del arbol de un padre especifico."""

        cb2 = Grupo.objects.get(id=3)
        lista_obtenida = Grupo.obtener_arbol(cb2)
        self.assertListEqual(lista_obtenida, self.lista_arbol_cb2)
