import factory
from common.tests.base import BaseTest
from iglesias.tests.factories import IglesiaFactory
from .factories import EmpleadoFactory, DepartamentoFactory


class CrearEmpleadoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista de creación de empleados de una iglesia.
    """

    URL = 'organizacional:empleado_nuevo'

    def setUp(self):
        self.admin = EmpleadoFactory(admin=True)
        self.login_usuario(self.admin.usuario)

    def datos_formulario(self, **kwargs):
        """
        Retorna un diccionario con los datos para el formulario NuevoEmpleadoForm.
        """

        self.departamento = DepartamentoFactory()
        data = factory.build(dict, FACTORY_CLASS=EmpleadoFactory)
        data.update({
            'email': 'a@a.com', 'contrasena1': 'mariana', 'contrasena2': 'mariana',
            'password2': 'mariana', 'departamento': self.departamento.id, 'jefe_departamento': True
        })
        data.update(**kwargs)
        return data

    def test_admin_get(self):
        """
        Prueba que el administrador pueda ver el template.
        """

        self.get_check_200(self.URL)
        self.assertResponseContains('id_cedula', html=False)

    def test_post_formulario_valido_crea_empleado_iglesia_correcta(self):
        """
        Prueba que cuando se haga un POST y el formulario sea valido el empleado creado pertenezca a la iglesia del
        usuario logueado.
        """
        from ..models import Empleado

        data = self.datos_formulario()
        iglesia_correcta = self.admin.iglesia
        iglesia_incorrecta = IglesiaFactory(nombre='nueva iglesia')

        self.login_usuario(self.admin.usuario)
        self.post(self.URL, data=data)

        empleado = Empleado.objects.get(cedula=data['cedula'])
        self.assertEqual(iglesia_correcta, empleado.iglesia)
        self.assertNotEqual(iglesia_incorrecta, empleado.iglesia)

    def test_admin_post_formulario_invalido_muestra_errores(self):
        """
        Prueba que cuando se haga POST y el formulario esta invalido se muestren los errores.
        """

        response = self.post(self.URL, data={})

        self.assertFormError(response, 'form', 'cargo', self.MSJ_OBLIGATORIO)
        self.assertFormError(response, 'form', 'email', self.MSJ_OBLIGATORIO)
        self.assertFormError(response, 'form', 'cedula', self.MSJ_OBLIGATORIO)
        self.assertFormError(response, 'form', 'departamento', self.MSJ_OBLIGATORIO)
        self.assertFormError(response, 'form', 'primer_nombre', self.MSJ_OBLIGATORIO)
        self.assertFormError(response, 'form', 'primer_apellido', self.MSJ_OBLIGATORIO)

    def test_admin_post_formulario_valido_redirecciona(self):
        """
        Prueba que cuando se haga POST y el formulario sea valido redireccione.
        """

        response = self.post(self.URL, data=self.datos_formulario())
        self.assertRedirects(response, self.reverse(self.URL))


class ListarEmpleadoViewTest(BaseTest):
    """
    Pruebas unitarias para la vista listar empleados de una iglesia.
    """

    URL = 'organizacional:empleado_listar'

    def setUp(self):
        self.empleado = EmpleadoFactory(admin=True)
        self.iglesia = self.empleado.iglesia

    def test_get_muestra_empleado_iglesia_correcta(self):
        """
        Prueba que se muestren los empleados de la iglesia correcta.
        """

        iglesia_incorrecta = IglesiaFactory(nombre='CDR')
        empleado2 = EmpleadoFactory(iglesia=iglesia_incorrecta)

        self.login_usuario(self.empleado.usuario)
        self.get_check_200(self.URL)

        self.assertResponseContains(self.empleado.cedula, html=False)
        self.assertResponseNotContains(empleado2.cedula, html=False)
