# Django imports
from django.core.urlresolvers import reverse

from common.tests.base import BaseTestAPI
from common import constants
from grupos.models import Grupo
from .factories import MiembroFactory

from unittest import mock


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
