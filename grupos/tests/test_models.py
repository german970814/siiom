from django.test import TestCase
from .factories import GrupoFactory, GrupoRaizFactory, GrupoHijoFactory
from grupos.models import Grupo


class GrupoModelTest(TestCase):

    def setUp(self):
        padre = GrupoRaizFactory(id=1)
        cabeza_red1 = GrupoFactory(id=2, parent=padre, red__nombre='matrimonio')
        cabeza_red2 = GrupoFactory(id=3, parent=padre)
        cabeza_red3 = GrupoFactory(id=4, parent=padre, red__nombre='adultos')

        hijo1_cb2 = GrupoHijoFactory(id=5, parent=cabeza_red2)
        hijo2_cb2 = GrupoHijoFactory(id=8, parent=cabeza_red2)
        hijo11_cb2 = GrupoHijoFactory(id=6, parent=hijo1_cb2)

        hijo1_cb3 = GrupoHijoFactory(id=7, parent=cabeza_red3)

        self.lista_arbol_completo = [
            padre, [cabeza_red1, cabeza_red2, [hijo1_cb2, [hijo11_cb2], hijo2_cb2], cabeza_red3, [hijo1_cb3]]
        ]

        self.lista_arbol_cb2 = [
            cabeza_red2, [hijo1_cb2, [hijo11_cb2], hijo2_cb2]
        ]

    def test_obtener_arbol_completo(self):
        """Lista obtenida sea igual a la lista del arbol completo."""

        lista_obtenida = Grupo.obtener_arbol()
        self.assertListEqual(lista_obtenida, self.lista_arbol_completo)

    def test_obtener_arbol_padre_especifico(self):
        """Lista obtenida sea igual a la lista del arbol de un padre especifico."""

        cb2 = Grupo.objects.get(id=3)
        lista_obtenida = Grupo.obtener_arbol(cb2)
        self.assertListEqual(lista_obtenida, self.lista_arbol_cb2)
