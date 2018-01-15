from unittest import mock
from django.test import tag
from common.tests.base import BaseTestAPI
from .factories import GrupoFactory, GrupoHijoFactory


class LideresGrupoTest(BaseTestAPI):
    """
    Pruebas unitarias para la vista lideres de un grupo.
    """

    def test_get_lideres_grupo(self):
        """
        Prueba que me devuelva solo los lideres del grupo ingresado.
        """

        grupo = GrupoFactory()
        self.url = self.reverse('grupos:lideres_api', grupo.pk)
        response = self.GET()

        self.assertEqual(grupo.lideres.first().pk, response[0]['pk'])


class DiscipulosGrupoViewTest(BaseTestAPI):
    """Pruebas unitarias para la vista discipulos de un grupo."""

    URL = 'grupos:discipulos_api'

    @mock.patch('grupos.models.Grupo.discipulos', new_callable=mock.PropertyMock)
    def test_get_discipulos_grupo(self, discipulos_mock):
        """Prueba que solo devuelva los discipulos del grupo ingresado."""

        grupo = GrupoFactory()
        self.url = self.reverse(self.URL, grupo.pk)
        self.GET()
        
        self.assertTrue(discipulos_mock.called)