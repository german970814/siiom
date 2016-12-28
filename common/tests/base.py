from django.test.client import Client
from test_plus.test import TestCase
from grupos.tests.factories import GrupoRaizFactory, GrupoHijoFactory, GrupoFactory
from .factories import UsuarioFactory
from .. import constants

import json


class BaseTest(TestCase):
    """
    Clase base para las pruebas unitarias.
    """

    MSJ_OBLIGATORIO = 'Este campo es obligatorio.'
    user_factory = UsuarioFactory

    def crear_arbol(self):
        """
        Crea un arbol para realizar las pruebas. Se muestra el arbol segun los ids de los grupos.

                 100
            |-----|-----|
            |     |     |
           200   300   400
                  |     |
                  |    700
                  |
             |---------|
            500       800
             |
            600
        """

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

    def login_usuario(self, usuario):
        """
        Permite loguear un usuario.
        """

        self.client.login(email=usuario.email, password='123456')


class APIClient(Client):
    """Cliente para API."""

    def get(self, follow=True, *args, **kwargs):
        response = super().get(follow=follow, *args, **kwargs)

        assert response._headers['content-type'][1].split(';')[0] == constants.CONTENT_TYPE_API

        return response

    def post(self, follow=True, *args, **kwargs):
        response = super().post(follow=follow, *args, **kwargs)

        assert response._headers['content-type'][1].split(';')[0] == constants.CONTENT_TYPE_API

        return response


class BaseTestAPI(BaseTest):
    """Clase de pruebas base para la API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = APIClient()

    def _GET(self, login=True, *args, **kwargs):
        if login:
            self.usuario = UsuarioFactory()
            self.login_usuario(self.usuario)
        url = kwargs.pop('url', None) or self.get_url()
        return self.client.get(url, *args, **kwargs)

    def _POST(self, login=True, *args, **kwargs):
        if login:
            self.usuario = UsuarioFactory()
            self.login_usuario(self.usuario)
        url = kwargs.pop('url', None) or self.get_url()
        return self.client.post(url, *args, **kwargs)

    def GET(self, *args, **kwargs):
        encoding = kwargs.pop('encoding', 'utf-8')
        return self.get_json(self._GET(*args, **kwargs), encoding=encoding)

    def POST(self, *args, **kwargs):
        encoding = kwargs.pop('encoding', 'utf-8')
        return self.get_json(self._POST(*args, **kwargs), encoding=encoding)

    def get_url(self):
        return self.url

    def get_json(self, response, encoding='utf-8'):
        from django.http import HttpResponse

        self.assertIn(HttpResponse, response.__class__.__mro__)

        return json.loads(response.content.decode(encoding))
