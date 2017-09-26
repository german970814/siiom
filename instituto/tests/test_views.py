from django.core.urlresolvers import reverse
from common.tests.base import BaseTest
from common.tests.factories import UsuarioFactory
from waffle.testutils import override_switch


class ReporteInstitutoTestView(BaseTest):

    def setUp(self):
        self.crear_arbol()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))
        self.URL = reverse('instituto:reporte_instituto')

    @override_switch('instituto', active=True)
    def test_retorne_html_con_formulario_invalido(self):
        """
        Prueba que con un POST y con errores en el formulario, se muestran los errores
        y la respuesta es un html.
        """
        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {})

        self.assertTrue(response._headers['content-type'][1].startswith('text/html'))
        self.assertFormError(response, 'form', 'grupo', self.MSJ_OBLIGATORIO)

    @override_switch('instituto', active=True)
    def test_retorne_excel_con_formulario_valido(self):
        """
        Prueba que cuando el formulario se envia correcto, la respuesta sera un archivo
        binario de excel.
        """
        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {'grupo': 100})

        self.assertTrue(response._headers['content-type'][1].startswith('application/vnd.ms-excel'))
