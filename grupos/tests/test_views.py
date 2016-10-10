from unittest import mock
from django.http import Http404
from django.test import TestCase
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, Group
from common.tests.factories import UsuarioFactory
from miembros.tests.factories import MiembroFactory, BarrioFactory
from miembros.models import Miembro
from grupos.models import Grupo, Red
from grupos.forms import GrupoRaizForm, NuevoGrupoForm, TransladarGrupoForm
from .factories import GrupoRaizFactory
from .base import GruposBaseTest


class OrganigramaGruposViewTest(GruposBaseTest):
    """
    Pruebas unitarias para la vista de organigrama de la red de grupos. Si un administrador entra a la vista podra ver
    todo el organigrama de la iglesia.
    """

    TEMPLATE = 'grupos/organigrama_grupos.html'
    URL = reverse('grupos:organigrama')

    def setUp(self):
        super(OrganigramaGruposViewTest, self).setUp()

    def ingresar_pagina(self, login=True):
        """
        Ingresa a la página del organigrama de grupos y retorna el reponse. Por defecto loguea al usuario.
        """

        if login:
            self.login_usuario()
        return self.client.get(self.URL)

    def test_usuario_no_logueado_redireccionado_login(self):
        """
        Prueba que un usuario no logueado sea redireccionado al login.
        """

        response = self.ingresar_pagina(login=False)
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('inicio'), self.URL))

    def test_usuario_logueado_no_lider_ni_admin_redireccionado_sin_permisos(self):
        """
        Prueba que un usuario logueado que no sea administrador ni líder sea redireccionado a página que indique que
        no tiene permisos.
        """

        response = self.ingresar_pagina()
        self.assertEqual(response.status_code, 403)

    def test_admin_vea_arbol_grupos_completo(self):
        """
        Prueba que un administrador pueda ver el arbol completo de la iglesia.
        """

        self.usuario.user_permissions.add(Permission.objects.get(codename='es_administrador'))
        response = self.ingresar_pagina()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)
        self.assertListEqual(response.context['arbol'], self.lista_arbol_completo)

    def test_lider_vea_arbol_desde_grupo_lidera(self):
        """
        Prueba que un líder solo pueda ver el arbol desde su grupo hacia abajo.
        """

        self.usuario.user_permissions.add(Permission.objects.get(codename='es_lider'))
        miembro = Grupo.objects.get(id=300).lideres.first()
        miembro.usuario = self.usuario
        miembro.save()

        response = self.ingresar_pagina()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)
        self.assertListEqual(response.context['arbol'], self.lista_arbol_cb2)


class GrupoRaizViewTest(TestCase):
    """
    Pruebas unitarias para la vista de creación/edición del grupo raiz.
    """

    URL = reverse('grupos:raiz')

    def setUp(self):
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))
        self.lider1 = MiembroFactory(lider=True)
        self.lider2 = MiembroFactory(lider=True)
        self.barrio = BarrioFactory()

    def login_usuario(self, usuario):
        """
        Loguea un usuario.
        """

        self.client.login(email=usuario.email, password='123456')

    def datos_formulario(self):
        """
        Retorna un diccionario con datos para el formulario GrupoRaiz.
        """

        data = {
            'direccion': 'Calle 34 N 74 - 23', 'estado': 'A', 'fechaApertura': '2012-03-03', 'diaGAR': '1',
            'horaGAR': '12:00', 'diaDiscipulado': '3', 'horaDiscipulado': '16:00', 'nombre': 'Pastor presidente',
            'barrio': self.barrio.id, 'lideres': [self.lider1.id]
        }

        return data

    def test_admin_get_template(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id_lideres')

    def test_get_no_existe_grupo_raiz_muestra_formulario_vacio(self):
        """
        Prueba que se muestre el formulario vacío, cuando no existe grupo raiz.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        self.assertIsInstance(response.context['form'], GrupoRaizForm)
        self.assertIsNone(response.context['form'].instance.pk)

    def test_get_existe_grupo_raiz_muestra_formulario_con_raiz(self):
        """
        Prueba que se muestre la información del grupo raiz si este ya existe.
        """

        raiz = GrupoRaizFactory()
        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        self.assertIsInstance(response.context['form'], GrupoRaizForm)
        self.assertEqual(response.context['form'].instance, raiz)

    def test_post_formulario_valido_redirecciona_get(self):
        """
        Prueba que si se hace un POST y el formulario es valido redirecciona a misma página en GET.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, self.datos_formulario())

        self.assertRedirects(response, self.URL)

    def test_formulario_invalido_muestra_errores(self):
        """
        Prueba que si el formulario no es valido se muestren los errores.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {})

        self.assertFormError(response, 'form', 'lideres', 'Este campo es obligatorio.')

    @mock.patch('django.db.models.query.QuerySet.update', side_effect=IntegrityError)
    def test_post_save_formulario_devuelve_None_muestra_error(self, update_mock):
        """
        Prueba que si cuando se guarda el formulario, este devuelve None se muestre un mensaje de error.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, self.datos_formulario())

        self.assertTrue(update_mock.called)
        self.assertFormError(response, 'form', None, GrupoRaizForm.mensaje_error)


class CrearGrupoViewTest(GruposBaseTest):
    """
    Pruebas unitarias para la vista creación de grupos.
    """

    def setUp(self):
        super(CrearGrupoViewTest, self).setUp()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))
        self.padre = Grupo.objects.get(id=800)
        self.lider1 = MiembroFactory(lider=True, grupo=self.padre)
        self.lider2 = MiembroFactory(lider=True, grupo=self.padre)
        self.barrio = BarrioFactory()

        red_jovenes = Red.objects.get(nombre='jovenes')
        self.URL = reverse('grupos:nuevo', args=(red_jovenes.id,))

    def login_usuario(self, usuario):
        """
        Loguea un usuario.
        """

        self.client.login(email=usuario.email, password='123456')

    def datos_formulario(self):
        """
        Retorna un diccionario con datos para el formulario GrupoForm.
        """

        data = {
            'direccion': 'Calle 34 N 74 - 23', 'estado': 'A', 'fechaApertura': '2012-03-03', 'diaGAR': '1',
            'horaGAR': '12:00', 'diaDiscipulado': '3', 'horaDiscipulado': '16:00', 'nombre': 'Pastor presidente',
            'barrio': self.barrio.id, 'lideres': [self.lider1.id, self.lider2.id], 'parent': self.padre.id
        }

        return data

    def test_get_red_no_existe_devuelve_404(self):
        """
        Prueba que si se envia una red que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.admin)
        response = self.client.get(reverse('grupos:nuevo', args=(100,)))
        self.assertRaises(Http404)

    def test_admin_get_template(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id_parent')

    def test_post_formulario_valido_redirecciona_get(self):
        """
        Prueba que si se hace un POST y el formulario es valido redirecciona a misma página en GET.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, self.datos_formulario())

        self.assertRedirects(response, self.URL)

    def test_formulario_invalido_muestra_errores(self):
        """
        Prueba que si el formulario no es valido se muestren los errores.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {})

        self.assertFormError(response, 'form', 'lideres', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'parent', 'Este campo es obligatorio.')

    @mock.patch('django.db.models.query.QuerySet.update', side_effect=IntegrityError)
    def test_post_save_formulario_devuelve_None_muestra_error(self, update_mock):
        """
        Prueba que si cuando se guarda el formulario, este devuelve None se muestre un mensaje de error.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, self.datos_formulario())

        self.assertTrue(update_mock.called)
        self.assertFormError(response, 'form', None, NuevoGrupoForm.mensaje_error)


class EditarGrupoViewTest(GruposBaseTest):
    """
    Pruebas unitarias para la vista edición de grupos.
    """

    URL = reverse('grupos:editar', args=(600,))

    def setUp(self):
        super(EditarGrupoViewTest, self).setUp()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))
        self.padre = Grupo.objects.get(id=800)
        self.lider1 = MiembroFactory(lider=True, grupo=self.padre)
        self.lider2 = MiembroFactory(lider=True, grupo=self.padre)
        self.barrio = BarrioFactory()

        red_jovenes = Red.objects.get(nombre='jovenes')

    def login_usuario(self, usuario):
        """
        Loguea un usuario.
        """

        self.client.login(email=usuario.email, password='123456')

    def datos_formulario(self):
        """
        Retorna un diccionario con datos para el formulario GrupoForm.
        """

        data = {
            'direccion': 'Calle 34 N 74 - 23', 'estado': 'A', 'fechaApertura': '2012-03-03', 'diaGAR': '1',
            'horaGAR': '12:00', 'diaDiscipulado': '3', 'horaDiscipulado': '16:00', 'nombre': 'Pastor presidente',
            'barrio': self.barrio.id, 'lideres': [self.lider1.id, self.lider2.id], 'parent': self.padre.id
        }

        return data

    def test_get_grupo_no_existe_devuelve_404(self):
        """
        Prueba que si se envia un grupo que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.admin)
        response = self.client.get(reverse('grupos:editar', args=(1000,)))
        self.assertRaises(Http404)

    def test_admin_get_template(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id_parent')

    def test_post_formulario_valido_redirecciona_get(self):
        """
        Prueba que si se hace un POST y el formulario es valido redirecciona a misma página en GET.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, self.datos_formulario())

        self.assertRedirects(response, self.URL)

    def test_formulario_invalido_muestra_errores(self):
        """
        Prueba que si el formulario no es valido se muestren los errores.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {})

        self.assertFormError(response, 'form', 'lideres', 'Este campo es obligatorio.')
        # self.assertFormError(response, 'form', 'parent', 'Este campo es obligatorio.')

    @mock.patch('django.db.models.query.QuerySet.update', side_effect=IntegrityError)
    def test_post_save_formulario_devuelve_None_muestra_error(self, update_mock):
        """
        Prueba que si cuando se guarda el formulario, este devuelve None se muestre un mensaje de error.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, self.datos_formulario())

        self.assertTrue(update_mock.called)
        self.assertFormError(response, 'form', None, NuevoGrupoForm.mensaje_error)


class TransladarGrupoViewTest(GruposBaseTest):
    """
    Pruebas unitarias para la vista de transladar un grupo a un nuevo padre.
    """

    TEMPLATE = 'grupos/transladar.html'
    URL = reverse('grupos:transladar', args=(500,))

    def setUp(self):
        super(TransladarGrupoViewTest, self).setUp()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))

    def login_usuario(self, usuario):
        """
        Loguea un usuario.
        """

        self.client.login(email=usuario.email, password='123456')

    def test_usuario_no_logueado_redireccionado_login(self):
        """
        Prueba que un usuario no logueado sea redireccionado a login.
        """

        response = self.client.get(self.URL)
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('inicio'), self.URL))

    def test_usuario_logueado_no_admin_redireccionado_sin_permisos(self):
        """
        Prueba que un usuario logueado que no sea administrador sea redireccionado a página que indique que
        no tiene permisos.
        """

        usuario = UsuarioFactory()
        self.login_usuario(usuario)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403)

    def test_get_grupo_no_existe_devuelve_404(self):
        """
        Prueba que cuando se envia el id de un grupo que no existe en la URL, la vista devuelve un 404.
        """

        self.login_usuario(self.admin)
        response = self.client.get(reverse('grupos:transladar', args=(100,)))
        self.assertRaises(Http404)

    def test_admin_get_template(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)
        self.assertIsInstance(response.context['form'], TransladarGrupoForm)

    def test_post_formulario_valido_translada_grupo(self):
        """
        Prueba que si el formulario es valido translada el  grupo y redirecciona.
        """

        nuevo = Grupo.objects.get(id=800)
        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {'nuevo': '800'})

        grupo = Grupo.objects.get(id=500)
        self.assertRedirects(response, self.URL)
        self.assertEqual(grupo.get_parent(), nuevo)

    def test_post_formulario_no_valido_muestra_errores(self):
        """
        Prueba que si el formulario no es valido se muestren los errores.
        """

        self.login_usuario(self.admin)
        response = self.client.post(self.URL, {})
        self.assertFormError(response, 'form', 'nuevo', 'Este campo es obligatorio.')
