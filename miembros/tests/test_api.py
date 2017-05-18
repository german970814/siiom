from unittest import mock

# Django imports
from django.core.urlresolvers import reverse

from common.tests.base import BaseTestAPI
from common.tests.factories import UsuarioFactory
from common import constants
from grupos.models import Grupo
from .factories import MiembroFactory


class DesvincularLiderGrupoAPITest(BaseTestAPI):
    """
    Pruebas unitarias para la vista de api de desvincular_lider_de_grupo_api.
    """

    def setUp(self):
        self.crear_arbol()
        self.grupo = Grupo.objects.get(id=300)
        self.miembro = MiembroFactory(lider=True, grupo=self.grupo.parent)
        self.url = reverse('miembros:desvincular_grupo_api', args=(self.grupo.lideres.first().id, ))

    def test_form_ivalid_response_es_json(self):
        """
        Verifica que en los errores, la respuesta sea de JSON
        """

        response = self.POST(login=True, kwargs_user={'admin': True})

        self.assertEqual(response[constants.RESPONSE_CODE], constants.RESPONSE_DENIED)
        self.assertIn('lider', response['errors'])

    def test_get_request_is_json(self):
        """
        Verifica que la respuesta en GET sea JSON
        """
        response = self.GET(login=True, kwargs_user={'admin': True})

        self.assertEqual(response[constants.RESPONSE_CODE], constants.RESPONSE_DENIED)

    @mock.patch('miembros.forms.DesvincularLiderGrupoForm.desvincular_lider', side_effect=None)
    def test_form_valid_llama_a_desvincular_grupo(self, desvincular_lider):
        """
        Verifica que el metodo de desvincular_lider de el formulario de DesvincularLiderGrupoForm
        sea llamado desde la api
        """

        self.POST(login=True, kwargs_user={'admin': True}, data={'lider': self.miembro.id})

        self.assertTrue(desvincular_lider.called)


class ResetearContrasenaAPITest(BaseTestAPI):
    """Pruebas unitarias para la vista que permite a un administrador resetar la contresaña de un miembro."""

    url = reverse('miembros:resetear_contrasena_api')

    def setUp(self):
        self.admin = UsuarioFactory(admin=True)
        self.miembro = MiembroFactory(lider=True)

    def test_get_resetear_contrasena_retorna_404(self):
        """Prueba que si se intenta hacer una petición GET retorne 404"""

        self.login_usuario(self.admin)
        response = self.GET()

        self.assertEqual(response[constants.RESPONSE_CODE], constants.RESPONSE_DENIED)

    @mock.patch('miembros.models.Miembro.resetear_contrasena')
    def test_post_resetear_contrasena(self, reset_mock):
        """Prueba que cuando un administrador haga POST se resetee la contraseña del miembro."""

        self.login_usuario(self.admin)
        self.POST(data={'miembro': self.miembro.pk})

        self.assertTrue(reset_mock.called)

    def test_form_invalid_response_es_json(self):
        """
        Verifica que en los errores, la respuesta sea de JSON
        """

        self.login_usuario(self.admin)
        response = self.POST(data={'miembro': 345})

        self.assertEqual(response[constants.RESPONSE_CODE], constants.RESPONSE_DENIED)
        self.assertIn('miembro', response['errors'])
