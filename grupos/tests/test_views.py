from unittest import mock
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from common.tests.base import BaseTest
from common.tests.factories import UsuarioFactory
from iglesias.tests.factories import IglesiaFactory
from miembros.tests.factories import MiembroFactory, BarrioFactory
from ..models import Grupo, Red
from ..forms import GrupoRaizForm, NuevoGrupoForm, TrasladarGrupoForm
from .factories import GrupoRaizFactory, ReunionGARFactory, GrupoFactory, ReunionDiscipuladoFactory, RedFactory


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

        miembro = Grupo.objects.get(id=300).lideres.first()
        self.login_usuario(miembro.usuario)
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)
        self.assertListEqual(response.context['arbol'], self.lista_arbol_cb2)


class GrupoRaizViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de creación/edición del grupo raiz.
    """

    URL = 'grupos:raiz'

    def setUp(self):
        self.admin = UsuarioFactory(admin=True)
        self.lider1 = MiembroFactory(lider=True)
        self.lider2 = MiembroFactory(lider=True)
        self.barrio = BarrioFactory()

    def datos_formulario(self):
        """
        Retorna un diccionario con datos para el formulario GrupoRaiz.
        """

        data = {
            'direccion': 'Calle 34 N 74 - 23', 'estado': 'AC', 'fechaApertura': '2012-03-03', 'diaGAR': '1',
            'horaGAR': '12:00', 'diaDiscipulado': '3', 'horaDiscipulado': '16:00', 'nombre': 'Pastor presidente',
            'barrio': self.barrio.id, 'lideres': [self.lider1.id]
        }

        return data

    def test_admin_get_template(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        self.get_check_200(self.URL)

        self.assertResponseContains('id_lideres', html=False)

    def test_get_no_existe_grupo_raiz_muestra_formulario_vacio(self):
        """
        Prueba que se muestre el formulario vacío, cuando no existe grupo raiz.
        """

        self.login_usuario(self.admin)
        self.get(self.URL)

        self.assertIsNone(self.get_context('form').instance.pk)

    def test_get_existe_grupo_raiz_muestra_formulario_con_raiz(self):
        """
        Prueba que se muestre la información del grupo raiz si este ya existe.
        """

        raiz = GrupoRaizFactory()
        self.login_usuario(self.admin)
        self.get(self.URL)

        self.assertEqual(self.get_context('form').instance, raiz)

    def test_get_existe_grupo_raiz_muestra_grupo_iglesia_correcta(self):
        """
        Prueba que se muestre la información del grupo raiz de la iglesia del usuario logueado.
        """

        raiz_incorrecta = GrupoRaizFactory(iglesia__nombre='otra iglesia')
        raiz_correcta = GrupoRaizFactory()
        self.login_usuario(self.admin)
        self.get(self.URL)

        self.assertNotEqual(raiz_incorrecta.iglesia, self.admin.miembro_set.first().iglesia)
        self.assertEqual(self.get_context('form').instance, raiz_correcta)

    def test_formulario_valido_crea_grupo_raiz_iglesia_correcta(self):
        """
        Prueba que cuando se haga un POST y el formulario sea valido el grupo creado pertenezca a la iglesia del usuario
        logueado.
        """

        iglesia_correcta = self.admin.miembro_set.first().iglesia
        otro_iglesia = IglesiaFactory(nombre='nueva iglesia')

        self.login_usuario(self.admin)
        self.post(self.URL, data=self.datos_formulario())

        self.assertNotEqual(iglesia_correcta, otro_iglesia)
        self.assertIsNotNone(Grupo.objects.raiz(iglesia_correcta))

    def test_post_formulario_valido_redirecciona_get(self):
        """
        Prueba que si se hace un POST y el formulario es valido redirecciona a misma página en GET.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, data=self.datos_formulario())

        self.assertRedirects(response, self.reverse(self.URL))

    def test_formulario_invalido_muestra_errores(self):
        """
        Prueba que si el formulario no es valido se muestren los errores.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, data={})

        self.assertFormError(response, 'form', 'lideres', 'Este campo es obligatorio.')

    @mock.patch('django.db.models.query.QuerySet.update', side_effect=IntegrityError)
    def test_post_save_formulario_devuelve_None_muestra_error(self, update_mock):
        """
        Prueba que si cuando se guarda el formulario, este devuelve None se muestre un mensaje de error.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, data=self.datos_formulario())

        self.assertTrue(update_mock.called)
        self.assertFormError(response, 'form', None, GrupoRaizForm.mensaje_error)


class CrearGrupoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista creación de grupos.
    """

    URL = 'grupos:nuevo'

    def setUp(self):
        self.crear_arbol()
        self.admin = UsuarioFactory(admin=True)
        self.padre = Grupo.objects.get(id=800)
        self.lider1 = MiembroFactory(lider=True, grupo=self.padre)
        self.lider2 = MiembroFactory(lider=True, grupo=self.padre)
        self.barrio = BarrioFactory()

        self.red_jovenes = Red.objects.get(nombre='jovenes')

    def datos_formulario(self):
        """
        Retorna un diccionario con datos para el formulario GrupoForm.
        """

        data = {
            'direccion': 'Calle 34 N 74 - 23', 'estado': 'AC', 'fechaApertura': '2012-03-03', 'diaGAR': '1',
            'horaGAR': '12:00', 'diaDiscipulado': '3', 'horaDiscipulado': '16:00', 'nombre': 'Pastor presidente',
            'barrio': self.barrio.id, 'lideres': [self.lider1.id, self.lider2.id], 'parent': self.padre.id
        }

        return data

    def test_get_red_no_existe_devuelve_404(self):
        """
        Prueba que si se envia una red que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.admin)
        self.get(self.URL, pk=100)

        self.response_404()

    def test_get_red_iglesia_diferente_devuelve_404(self):
        """
        Prueba que si el usuario intenta crear un grupo en una red que no sea de su iglesia la vista devuelva un
        status de 404.
        """

        otra_red = RedFactory(nombre='nueva red', iglesia__nombre='nueva iglesia')
        self.login_usuario(self.admin)
        self.get(self.URL, pk=otra_red.id)

        self.assertNotEqual(otra_red.iglesia_id, self.red_jovenes.iglesia_id)
        self.response_404()

    def test_admin_get_template(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        self.get_check_200(self.URL, pk=self.red_jovenes.id)

        self.assertResponseContains('id_parent', html=False)

    def test_post_formulario_valido_redirecciona_get(self):
        """
        Prueba que si se hace un POST y el formulario es valido redirecciona a misma página en GET.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, pk=self.red_jovenes.id, data=self.datos_formulario())

        self.assertRedirects(response, self.reverse('grupos:listar', pk=self.red_jovenes.id))

    def test_formulario_invalido_muestra_errores(self):
        """
        Prueba que si el formulario no es valido se muestren los errores.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, pk=self.red_jovenes.id, data={})

        self.assertFormError(response, 'form', 'lideres', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'parent', 'Este campo es obligatorio.')

    @mock.patch('django.db.models.query.QuerySet.update', side_effect=IntegrityError)
    def test_post_save_formulario_devuelve_None_muestra_error(self, update_mock):
        """
        Prueba que si cuando se guarda el formulario, este devuelve None se muestre un mensaje de error.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, pk=self.red_jovenes.id, data=self.datos_formulario())

        self.assertTrue(update_mock.called)
        self.assertFormError(response, 'form', None, NuevoGrupoForm.mensaje_error)


class EditarGrupoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista edición de grupos.
    """

    URL = 'grupos:editar'

    def setUp(self):
        self.crear_arbol()
        self.admin = UsuarioFactory(admin=True)
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
            'direccion': 'Calle 34 N 74 - 23', 'estado': 'AC', 'fechaApertura': '2012-03-03', 'diaGAR': '1',
            'horaGAR': '12:00', 'diaDiscipulado': '3', 'horaDiscipulado': '16:00', 'nombre': 'Pastor presidente',
            'barrio': self.barrio.id, 'lideres': [self.lider1.id, self.lider2.id], 'parent': self.padre.id
        }

        return data

    def test_get_grupo_no_existe_devuelve_404(self):
        """
        Prueba que si se envia un grupo que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.admin)
        self.get(self.URL, pk=1000)

        self.response_404()

    def test_get_grupo_iglesia_diferente_devuelve_404(self):
        """
        Prueba que si el usuario intenta editar un grupo que no sea de su iglesia la vista devuelva un status de 404.
        """

        grupo = Grupo.objects.get(id=600)
        otro_grupo = GrupoFactory(iglesia__nombre='nueva iglesia')
        self.login_usuario(self.admin)
        self.get(self.URL, pk=otro_grupo.id)

        self.assertNotEqual(otro_grupo.iglesia_id, grupo.iglesia_id)
        self.response_404()

    def test_admin_get_template(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        self.get_check_200(self.URL, pk=600)

        self.assertResponseContains('id_parent', html=False)

    def test_post_formulario_valido_redirecciona_get(self):
        """
        Prueba que si se hace un POST y el formulario es valido redirecciona a misma página en GET.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, pk=600, data=self.datos_formulario())

        red = Grupo.objects.get(id=600).red
        self.assertRedirects(response, self.reverse('grupos:listar', pk=red.id))

    def test_formulario_invalido_muestra_errores(self):
        """
        Prueba que si el formulario no es valido se muestren los errores.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, pk=600, data={})

        self.assertFormError(response, 'form', 'lideres', self.MSJ_OBLIGATORIO)

    @mock.patch('django.db.models.query.QuerySet.update', side_effect=IntegrityError)
    def test_post_save_formulario_devuelve_None_muestra_error(self, update_mock):
        """
        Prueba que si cuando se guarda el formulario, este devuelve None se muestre un mensaje de error.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, pk=600, data=self.datos_formulario())

        self.assertTrue(update_mock.called)
        self.assertFormError(response, 'form', None, NuevoGrupoForm.mensaje_error)


class ListarGruposRedViewTest(BaseTest):
    """
    Pruebas unitarias para la vista listar grupos de una red especifica.
    """

    URL = 'grupos:listar'

    def setUp(self):
        self.crear_arbol()
        self.red = Red.objects.get(nombre='jovenes')
        # self.URL = reverse('grupos:listar', args=(red_jovenes.id,))
        self.admin = UsuarioFactory(admin=True)

    def test_get_red_no_existe_devuelve_404(self):
        """
        Prueba que si se envia una red que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.admin)
        self.get(self.URL, pk=100)
        self.response_404()

    def test_get_red_iglesia_diferente_devuelve_404(self):
        """
        Prueba que si el usuario intenta listar los grupos de una red que no sea de su iglesia la vista
        devuelva un status de 404.
        """

        otra_red = RedFactory(nombre='nueva red', iglesia__nombre='nueva iglesia')
        self.login_usuario(self.admin)
        self.get(self.URL, pk=otra_red.id)

        self.assertNotEqual(otra_red.iglesia_id, self.red.iglesia_id)
        self.response_404()

    def test_get_muestra_grupos_de_red(self):
        """
        Prueba que se listen los grupos de la red ingresada.
        """

        self.login_usuario(self.admin)
        self.get(self.URL, pk=self.red.pk)

        grupo_red = Grupo.objects.get(id=300)
        self.assertResponseContains(str(grupo_red), html=False)

    def test_get_no_muestra_grupos_red_diferente(self):
        """
        Prueba que no se muestren grupos que no pertenecen a la red ingresada.
        """

        self.login_usuario(self.admin)
        self.get(self.URL, pk=self.red.pk)

        otro_grupo = Grupo.objects.get(id=200)
        self.assertResponseNotContains(str(otro_grupo), html=False)


class TrasladarGrupoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de trasladar un grupo a un nuevo padre.
    """

    TEMPLATE = 'grupos/trasladar.html'
    URL = reverse('grupos:trasladar', args=(500,))

    def setUp(self):
        self.crear_arbol()
        self.admin = UsuarioFactory(user_permissions=('es_administrador',))

    def test_get_grupo_no_existe_devuelve_404(self):
        """
        Prueba que cuando se envia el id de un grupo que no existe en la URL, la vista devuelve un 404.
        """

        self.login_usuario(self.admin)
        response = self.client.get(reverse('grupos:trasladar', args=(1000,)))
        self.response_404(response)

    def test_admin_get_template(self):
        """
        Prueba que un administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.TEMPLATE)
        self.assertIsInstance(response.context['form'], TrasladarGrupoForm)

    def test_post_formulario_valido_traslada_grupo(self):
        """
        Prueba que si el formulario es valido traslada el  grupo y redirecciona.
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
        response = self.client.get(reverse('grupos:confirmar_ofrenda_GAR', args=(1000,)))
        self.response_404(response)

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
        response = self.client.get(reverse('grupos:confirmar_ofrenda_discipulado', args=(1000,)))
        self.response_404(response)

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
        response = self.client.get(reverse(self.URL_NAME, args=[1000]))
        self.response_404(response)

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


class CrearRedViewTest(BaseTest):
    """
    Pruebas unitarias para la vista crear red para una iglesia.
    """

    URL = 'grupos:red_nueva'

    def setUp(self):
        self.admin = UsuarioFactory(admin=True)

    def datos_formulario(self):
        return {'nombre': 'red'}

    def test_admin_get(self):
        """
        Prueba que el administrador pueda ver el template.
        """

        self.login_usuario(self.admin)
        self.get_check_200(self.URL)
        self.assertResponseContains('id_nombre', html=False)

    def test_formulario_valido_crea_red_iglesia_correcta(self):
        """
        Prueba que cuando se haga un POST y el formulario sea valido la red creada pertenezca a la iglesia del usuario
        logueado.
        """

        iglesia_correcta = self.admin.miembro_set.first().iglesia
        otro_iglesia = IglesiaFactory(nombre='nueva iglesia')

        self.login_usuario(self.admin)
        self.post(self.URL, data=self.datos_formulario())

        red = Red.objects.get(nombre='red')
        self.assertEqual(iglesia_correcta, red.iglesia)
        self.assertNotEqual(iglesia_correcta, otro_iglesia)

    def test_post_formulario_valido_redirecciona_get(self):
        """
        Prueba que si se hace un POST y el formulario es valido redirecciona a la misma página.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, data=self.datos_formulario())

        self.assertRedirects(response, self.reverse(self.URL))

    def test_formulario_invalido_muestra_errores(self):
        """
        prueba que si se hace POST y el formulario es invalido se muestren los errores correctamente.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, data={})

        self.assertFormError(response, 'form', 'nombre', self.MSJ_OBLIGATORIO)


class EditarRedViewTest(BaseTest):
    """
    Pruebas unitarias para la vista editar red de una iglesia.
    """

    URL = 'grupos:red_editar'

    def setUp(self):
        self.admin = UsuarioFactory(admin=True)
        self.red = RedFactory()

    def datos_formulario(self):
        return {'nombre': 'red editada'}

    def test_get_red_no_existe_devuelve_404(self):
        """
        Prueba que si se envia una red que no existe la vista devuelve un status code de 404.
        """

        self.login_usuario(self.admin)
        self.get('grupos:editar', pk=4000)

        self.response_404()

    def test_get_red_iglesia_diferente_devuelve_404(self):
        """
        Prueba que si el usuario intenta editar una red que no sea de su iglesia la vista devuelva un status de 404.
        """

        otra_red = RedFactory(nombre='nueva red', iglesia__nombre='nueva iglesia')
        self.login_usuario(self.admin)
        self.get(self.URL, pk=otra_red.id)

        self.assertNotEqual(otra_red.iglesia_id, self.red.iglesia_id)
        self.response_404()

    def test_admin_get_template(self):
        """
        Prueba que el administrador vea la página con GET.
        """

        self.login_usuario(self.admin)
        self.get_check_200(self.URL, pk=self.red.id)

        self.assertResponseContains('id_nombre', html=False)

    def test_post_formulario_valido_redirecciona_get(self):
        """
        Prueba que si se hace un POST y el formulario es valido redirecciona a la misma página.
        """

        data = self.datos_formulario()
        self.login_usuario(self.admin)
        response = self.post(self.URL, pk=self.red.id, data=data)

        self.red.refresh_from_db()
        self.assertEqual(self.red.nombre, data['nombre'])
        self.assertRedirects(response, self.reverse(self.URL, pk=self.red.id))

    def test_formulario_invalido_muestra_errores(self):
        """
        prueba que si se hace POST y el formulario es invalido se muestren los errores correctamente.
        """

        self.login_usuario(self.admin)
        response = self.post(self.URL, pk=self.red.id, data={})

        self.assertFormError(response, 'form', 'nombre', self.MSJ_OBLIGATORIO)


class ListarRedesViewTest(BaseTest):
    """
    Pruebas unitarias para la vista listar redes de una iglesia.
    """

    URL = 'grupos:redes_listar'

    def setUp(self):
        self.admin = UsuarioFactory(admin=True)

    def test_get_muestra_redes_iglesia_correcta(self):
        """
        Prueba que se listen las redes de la iglesia del usuario logueado.
        """

        red1 = RedFactory()
        red2 = RedFactory(nombre='adultos jovenes')
        red_incorrecta = RedFactory(nombre='otra red', iglesia__nombre='otra iglesia')

        self.login_usuario(self.admin)
        self.get_check_200(self.URL)

        self.assertResponseContains(red1.nombre.capitalize(), html=False)
        self.assertResponseContains(red2.nombre.capitalize(), html=False)
        self.assertResponseNotContains(red_incorrecta.nombre.capitalize(), html=False)


class TrasladarLideresViewTest(BaseTest):
    """
    Pruebas unitarias para la vista trasladar lideres de una iglesia.
    """

    URL = 'grupos:trasladar_lideres'

    def setUp(self):
        self.crear_arbol()
        admin = UsuarioFactory(admin=True)
        self.login_usuario(admin)

    def datos_formulario(self):
        lider = Grupo.objects.get(id=500).lideres.first()
        return {'grupo': '500', 'lideres': lider.pk, 'nuevo_grupo': '800'}

    def test_admin_get(self):
        """
        Prueba que un administrador pueda ver el formulario.
        """

        self.get_check_200(self.URL)
        self.assertResponseContains('id_grupo', html=False)

    @mock.patch('miembros.managers.MiembroManager.trasladar_lideres')
    def test_post_formulario_valido_traslada_lideres_escogidos(self, trasladar_mock):
        """
        Prueba que si se hace POST y el formulario es valido se trasladen los lideres o lider escogido.
        """

        self.post(self.URL, data=self.datos_formulario())
        self.assertTrue(trasladar_mock.called)

    def test_post_formulario_valido_redirecciona_organigrama(self):
        """
        Prueba que si se hace POST y el formulario es valido redirecciona a la vista del organigrama.
        """

        response = self.post(self.URL, data=self.datos_formulario())
        self.assertRedirects(response, self.reverse('grupos:organigrama'))

    def test_post_formulario_invalido_muestra_errores(self):
        """
        Prueba que si se hace POST y el formulario es invalido se muestren los errores.
        """

        response = self.post(self.URL, data={})
        self.assertFormError(response, 'form', 'grupo', self.MSJ_OBLIGATORIO)
        self.assertFormError(response, 'form', 'lideres', self.MSJ_OBLIGATORIO)
        self.assertFormError(response, 'form', 'nuevo_grupo', self.MSJ_OBLIGATORIO)
