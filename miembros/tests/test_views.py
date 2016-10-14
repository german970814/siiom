from django.http import Http404
from django.core.urlresolvers import reverse
from grupos.models import Red, Grupo
from common.tests.base import BaseTest
from common.tests.factories import UsuarioFactory


class ListarLideresRedViewTest(BaseTest):
    """
    Pruebas unitarias para la vista listar lideres de una red.
    """

    def setUp(self):
        self.crear_arbol()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))

        red_jovenes = Red.objects.get(nombre='jovenes')
        self.URL = reverse('miembros:listar_lideres', args=(red_jovenes.id,))

    def test_get_red_no_existe_devuelve_404(self):
        """
        Prueba que si se envia una red que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.admin)
        self.client.get(reverse('miembros:listar_lideres', args=(100,)))
        self.assertRaises(Http404)

    def test_get_muestra_lideres_red(self):
        """
        Prueba que se listen los lideres de la red escogida.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        lider = Grupo.objects.get(id=300).lideres.first()
        self.assertContains(response, lider.nombre.upper())
