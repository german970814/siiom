from django.http import Http404
from django.core.urlresolvers import reverse
from grupos.models import Red, Grupo
from grupos.tests.factories import GrupoFactory
from common.tests.base import BaseTest
from common.tests.factories import UsuarioFactory
from .factories import MiembroFactory


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


class TransladarMiembroViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de transladar un miembro que no lidere grupo a otro grupo.
    """

    def setUp(self):
        grupo1 = GrupoFactory()
        self.grupo2 = GrupoFactory()
        self.miembro = MiembroFactory(grupo=grupo1)
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))

        self.URL = reverse('miembros:transladar', args=(self.miembro.id,))

    def test_get_miembro_no_existe_devuelve_404(self):
        """
        Prueba que cuando se envia el id de un miembro que no existe en la URL, la vista devuelve un 404.
        """

        self.login_usuario(self.admin)
        self.client.get(reverse('miembros:transladar', args=(100,)))
        self.assertRaises(Http404)

    def test_get_miembro_lider_grupo_redirecciona_sin_permisos(self):
        """
        Prueba que si se intenta transladar un miembro que lidera un grupo se redireccione a página sin permisos.
        """

        self.login_usuario(self.admin)
        lider = self.grupo2.lideres.first()
        response = self.client.get(reverse('miembros:transladar', args=(lider.id,)))

        self.assertEqual(response.status_code, 302)

    def test_admin_get(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        self.assertContains(response, 'input')
        self.assertContains(response, self.miembro.nombre.upper())

    def test_post_formulario_valido_translada_miembro(self):
        """
        Prueba que si el formulario es valido translada el miembro y redirecciona.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {'nuevo': self.grupo2.id})
        self.miembro.refresh_from_db()

        self.assertRedirects(response, self.URL)
        self.assertEqual(self.miembro.grupo, self.grupo2)

    def test_post_formulario_no_valido_muestra_errores(self):
        """
        Prueba que si el formulario no es valido se muestren los errores.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {})
        self.assertFormError(response, 'form', 'nuevo', 'Este campo es obligatorio.')


class CrearMiembroViewTest(BaseTest):
    """
    Pruebas unitarias para la vista crear miembro de una iglesia.
    """

    URL = 'miembros:nuevo'

    def setUp(self):
        self.admin = MiembroFactory(admin=True)

    def test_admin_get(self):
        """
        Prueba que el administrador pueda ver el template.
        """

        self.login_usuario(self.admin.usuario)
        self.get_check_200(self.URL)
        self.assertResponseContains('id_nombre', html=False)
