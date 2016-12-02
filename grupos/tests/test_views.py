from unittest import mock
from django.http import Http404
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from common.tests.base import BaseTest
from common.tests.factories import UsuarioFactory
from miembros.tests.factories import MiembroFactory, BarrioFactory
from ..models import Grupo, Red
from ..forms import GrupoRaizForm, NuevoGrupoForm, TransladarGrupoForm
from .factories import GrupoRaizFactory, ReunionGARFactory, GrupoFactory, ReunionDiscipuladoFactory


class OrganigramaGruposViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de organigrama de la red de grupos. Si un administrador entra a la vista podra ver
    todo el organigrama de la iglesia.
    """

    TEMPLATE = 'grupos/organigrama_grupos.html'
    URL = reverse('grupos:organigrama')

    def setUp(self):
        self.crear_arbol()
        self.usuario = UsuarioFactory()

    def ingresar_pagina(self, login=True):
        """
        Ingresa a la página del organigrama de grupos y retorna el reponse. Por defecto loguea al usuario.
        """

        if login:
            self.login_usuario(self.usuario)
        return self.client.get(self.URL)

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


class GrupoRaizViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de creación/edición del grupo raiz.
    """

    URL = reverse('grupos:raiz')

    def setUp(self):
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))
        self.lider1 = MiembroFactory(lider=True)
        self.lider2 = MiembroFactory(lider=True)
        self.barrio = BarrioFactory()

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


class CrearGrupoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista creación de grupos.
    """

    def setUp(self):
        self.crear_arbol()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))
        self.padre = Grupo.objects.get(id=800)
        self.lider1 = MiembroFactory(lider=True, grupo=self.padre)
        self.lider2 = MiembroFactory(lider=True, grupo=self.padre)
        self.barrio = BarrioFactory()

        self.red_jovenes = Red.objects.get(nombre='jovenes')
        self.URL = reverse('grupos:nuevo', args=(self.red_jovenes.id,))

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
        self.client.get(reverse('grupos:nuevo', args=(100,)))
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

        self.assertRedirects(response, reverse('grupos:listar', args=(self.red_jovenes.id,)))

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


class EditarGrupoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista edición de grupos.
    """

    URL = reverse('grupos:editar', args=(600,))

    def setUp(self):
        self.crear_arbol()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))
        self.padre = Grupo.objects.get(id=800)
        self.lider1 = MiembroFactory(lider=True, grupo=self.padre)
        self.lider2 = MiembroFactory(lider=True, grupo=self.padre)
        self.barrio = BarrioFactory()

        Red.objects.get(nombre='jovenes')

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
        self.client.get(reverse('grupos:editar', args=(1000,)))
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

        red = Grupo.objects.get(id=600).red
        self.assertRedirects(response, reverse('grupos:listar', args=(red.id,)))

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


class ListarGruposRedViewTest(BaseTest):
    """
    Pruebas unitarias para la vista listar grupos de una red especifica.
    """

    def setUp(self):
        self.crear_arbol()
        red_jovenes = Red.objects.get(nombre='jovenes')
        self.URL = reverse('grupos:listar', args=(red_jovenes.id,))
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))

    def test_get_red_no_existe_devuelve_404(self):
        """
        Prueba que si se envia una red que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.admin)
        self.client.get(reverse('grupos:listar', args=(100,)))
        self.assertRaises(Http404)

    def test_get_muestra_grupos_de_red(self):
        """
        Prueba que se listen los grupos de la red ingresada.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        grupo_red = Grupo.objects.get(id=300)
        otro_grupo = Grupo.objects.get(id=200)
        self.assertContains(response, str(grupo_red))
        self.assertNotContains(response, str(otro_grupo))


class TransladarGrupoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de transladar un grupo a un nuevo padre.
    """

    TEMPLATE = 'grupos/transladar.html'
    URL = reverse('grupos:transladar', args=(500,))

    def setUp(self):
        self.crear_arbol()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))

    def test_get_grupo_no_existe_devuelve_404(self):
        """
        Prueba que cuando se envia el id de un grupo que no existe en la URL, la vista devuelve un 404.
        """

        self.login_usuario(self.admin)
        self.client.get(reverse('grupos:transladar', args=(100,)))
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


class SinConfirmarOfrendaGARViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de grupos sin confirmar ofrenda de las reuniones GAR.
    """

    URL = reverse('grupos:sin_confirmar_ofrenda_GAR')

    def test_get_muestra_grupos(self):
        """
        Prueba que se listen los grupos que faltan por confirmar ofrenda de la reunion GAR.
        """

        sin_confirmar = ReunionGARFactory()
        admin = UsuarioFactory(user_permissions=('es_administrador',))
        confirmada = ReunionGARFactory(confirmacionEntregaOfrenda=True)

        self.login_usuario(admin)
        response = self.client.get(self.URL)

        self.assertContains(response, str(sin_confirmar.grupo))
        self.assertNotContains(response, str(confirmada.grupo))


class ConfirmarOfrendaGARViewTest(BaseTest):
    """
    Pruebas unitarias para la vista para confirmar ofrendas de las reuniones GAR.
    """

    def setUp(self):
        self.usuario = UsuarioFactory(user_permissions=('puede_confirmar_ofrenda_GAR',))
        grupo = GrupoFactory()
        self.sin_confirmar = ReunionGARFactory(grupo=grupo)
        ReunionGARFactory(grupo=grupo, confirmacionEntregaOfrenda=True)

        self.URL = reverse('grupos:confirmar_ofrenda_GAR', args=(grupo.id,))

    def test_get_grupo_no_existe_devuelve_404(self):
        """
        Prueba que si se envia un grupo que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.usuario)
        self.client.get(reverse('grupos:confirmar_ofrenda_GAR', args=(1000,)))
        self.assertRaises(Http404)

    def test_get_muestra_reuniones_sin_confirmar(self):
        """
        Prueba que se listen las reuniones GAR del grupo escogido a las cuales no se les ha confirmado la ofrenda.
        """

        self.login_usuario(self.usuario)
        response = self.client.get(self.URL)

        self.assertContains(response, self.sin_confirmar.ofrenda)

    def test_post_confirma_ofrenda(self):
        """
        Prueba que si se hace un POST se confirmen las reuniones escogidas y redirecciona a la misma página con GET.
        """

        self.login_usuario(self.usuario)
        response = self.client.post(self.URL, {'seleccionados': [self.sin_confirmar.id]})

        self.sin_confirmar.refresh_from_db()
        self.assertRedirects(response, self.URL)
        self.assertTrue(self.sin_confirmar.confirmacionEntregaOfrenda)


class SinConfirmarOfrendaDiscipuladoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de grupos sin confirmar ofrenda de las reuniones de discipulado.
    """

    URL = reverse('grupos:sin_confirmar_ofrenda_discipulado')

    def test_get_muestra_grupos(self):
        """
        Prueba que se listen los grupos que faltan por confirmar ofrenda de la reunion discipulado.
        """

        sin_confirmar = ReunionDiscipuladoFactory()
        admin = UsuarioFactory(user_permissions=('es_administrador',))
        confirmada = ReunionDiscipuladoFactory(confirmacionEntregaOfrenda=True)

        self.login_usuario(admin)
        response = self.client.get(self.URL)

        self.assertContains(response, str(sin_confirmar.grupo))
        self.assertNotContains(response, str(confirmada.grupo))


class ConfirmarOfrendaDiscipuladoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista para confirmar ofrendas de las reuniones de discipulado.
    """

    def setUp(self):
        self.usuario = UsuarioFactory(user_permissions=('puede_confirmar_ofrenda_discipulado',))
        grupo = GrupoFactory()
        self.sin_confirmar = ReunionDiscipuladoFactory(grupo=grupo)
        ReunionDiscipuladoFactory(grupo=grupo, confirmacionEntregaOfrenda=True)

        self.URL = reverse('grupos:confirmar_ofrenda_discipulado', args=(grupo.id,))

    def test_get_grupo_no_existe_devuelve_404(self):
        """
        Prueba que si se envia un grupo que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.usuario)
        self.client.get(reverse('grupos:confirmar_ofrenda_discipulado', args=(1000,)))
        self.assertRaises(Http404)

    def test_get_muestra_reuniones_sin_confirmar(self):
        """
        Prueba que se listen las reuniones de discipulado del grupo escogido a las cuales no se les ha confirmado la
        ofrenda.
        """

        self.login_usuario(self.usuario)
        response = self.client.get(self.URL)

        self.assertContains(response, self.sin_confirmar.ofrenda)

    def test_post_confirma_ofrenda(self):
        """
        Prueba que si se hace un POST se confirmen las reuniones escogidas y redirecciona a la misma página con GET.
        """

        self.login_usuario(self.usuario)
        response = self.client.post(self.URL, {'seleccionados': [self.sin_confirmar.id]})

        self.sin_confirmar.refresh_from_db()
        self.assertRedirects(response, self.URL)
        self.assertTrue(self.sin_confirmar.confirmacionEntregaOfrenda)


class DetalleGrupoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de detalle de un grupo.
    """

    URL_NAME = 'grupos:detalle'

    def setUp(self):
        self.usuario = UsuarioFactory(user_permissions=['buscar_todos'])

    def test_get_grupo_no_existe_devuelve_404(self):
        """
        Prueba que si se envia un grupo que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.usuario)
        self.client.get(reverse(self.URL_NAME, args=[1000]))
        self.assertRaises(Http404)

    def test_get_grupo_muestra_info_grupo(self):
        """
        prueba que se muestre la información del grupo ingresado.
        """

        grupo = GrupoFactory()
        self.login_usuario(self.usuario)
        response = self.client.get(reverse(self.URL_NAME, args=[grupo.id]))

        self.assertContains(response, str(grupo))

    def test_lider_get_grupo_no_descendiente_devuelve_403(self):
        """
        Prueba que si el usuario no tiene el permiso buscar_todos y grupo ingresado no hace parte de sus descendientes
        devuelva permiso denegado.
        """

        self.crear_arbol()
        grupo = Grupo.objects.get(id=300)
        lider = grupo.lideres.first()

        self.login_usuario(lider.usuario)
        response = self.client.get(reverse(self.URL_NAME, args=[100]))
        self.assertEqual(response.status_code, 403)

    def test_lider_sin_grupo_devuelve_403(self):
        """
        Prueba que si el usuario no lidera grupo y no tiene el permiso buscar_todos devuelva permiso denegado.
        """

        grupo = GrupoFactory()
        lider = MiembroFactory(lider=True)
        self.login_usuario(lider.usuario)
        response = self.client.get(reverse(self.URL_NAME, args=[grupo.id]))

        self.assertEqual(response.status_code, 403)
