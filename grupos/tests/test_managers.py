from django.test import TestCase
from grupos.models import Grupo
from .factories import GrupoRaizFactory, GrupoFactory


class GrupoManagerTest(TestCase):
    """
    Pruebas unitarias para el manager de grupos.
    """

    def test_obtener_raiz_arbol(self):
        """
        Prueba que el grupo obtenido sea la raiz del arbol.
        """

        raiz = GrupoRaizFactory()
        no_raiz = GrupoFactory(parent=raiz)

        raiz_obtenida = Grupo.objects.raiz()
        self.assertEqual(raiz_obtenida, raiz)

    def test_no_hay_raiz_arbol_devuelva_none(self):
        """
        Prueba que si no hay grupo raiz en el arbol de grupos devuelva None.
        """

        raiz_obtenida = Grupo.objects.raiz()
        self.assertIsNone(raiz_obtenida)
