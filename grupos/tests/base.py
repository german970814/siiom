from django.test import TestCase
from common.tests.factories import UsuarioFactory
from .factories import GrupoFactory, GrupoRaizFactory, GrupoHijoFactory


class GruposBaseTest(TestCase):
    """
    Clase base para las pruebas de la app grupos.
    """

    def setUp(self):
        padre = GrupoRaizFactory(id=100)
        cabeza_red1 = GrupoFactory(id=200, parent=padre, red__nombre='matrimonio')
        cabeza_red2 = GrupoFactory(id=300, parent=padre)
        cabeza_red3 = GrupoFactory(id=400, parent=padre, red__nombre='adultos')

        hijo1_cb2 = GrupoHijoFactory(id=500, parent=cabeza_red2)
        hijo2_cb2 = GrupoHijoFactory(id=800, parent=cabeza_red2)
        hijo11_cb2 = GrupoHijoFactory(id=600, parent=hijo1_cb2)

        hijo1_cb3 = GrupoHijoFactory(id=700, parent=cabeza_red3)

        self.lista_arbol_completo = [
            padre, [cabeza_red1, cabeza_red2, [hijo1_cb2, [hijo11_cb2], hijo2_cb2], cabeza_red3, [hijo1_cb3]]
        ]

        self.lista_arbol_cb2 = [
            cabeza_red2, [hijo1_cb2, [hijo11_cb2], hijo2_cb2]
        ]

        self.usuario = UsuarioFactory()

    def login_usuario(self):
        """"Permite loguear al usuario."""

        self.client.login(email=self.usuario.email, password='123456')
