from django.test import TestCase
from .factories import GrupoFactory, GrupoRaizFactory


class GrupoModelTest(TestCase):

    def crear_arbol(self):
        padre = GrupoRaizFactory(id=1)
        cabeza_red1 = GrupoFactory(id=2, parent=padre)
        cabeza_red2 = GrupoFactory(id=3, parent=padre)
        cabeza_red3 = GrupoFactory(id=4, parent=padre)

        hijo1_cb2 = GrupoFactory(id=5, parent=cabeza_red2)
        hijo2_cb2 = GrupoFactory(id=8, parent=cabeza_red2)
        hijo11_cb2 = GrupoFactory(id=6, parent=hijo1_cb2)

        hijo1_cb3 = GrupoFactory(id=7, parent=cabeza_red3)

    def test_obtener_arbol(self):
        """"""

        self.crear_arbol()
