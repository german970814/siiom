from common.tests.base import BaseTest
from grupos.models import Grupo
from grupos.tests.factories import GrupoFactory
from .factories import MiembroFactory


class MiembroModelTest(BaseTest):
    """
    Pruebas unitarias para el modelo Miembro.
    """

    def test_es_director_red(self):
        """Prueba que si el miembro es director de red devuelva True."""

        self.crear_arbol()
        director = Grupo.objects.get(id=200).lideres.first()
        no_director = Grupo.objects.get(id=500).lideres.first()

        self.assertTrue(director.es_director_red)
        self.assertFalse(no_director.es_director_red)

    def test_trasladar_miembro_mismo_grupo(self):
        """Prueba que cuando se quiere trasladar un miembro al mismo grupo no se cambie el grupo actual."""

        grupo = GrupoFactory()
        miembro = MiembroFactory(grupo=grupo)

        miembro.trasladar(grupo)
        miembro.refresh_from_db()
        self.assertEqual(miembro.grupo, grupo)

    def test_trasladar_miembro_mueve(self):
        """Prueba que se traslada un miembro a un nuevo grupo."""

        grupo1 = GrupoFactory()
        grupo2 = GrupoFactory()
        miembro = MiembroFactory(grupo=grupo1)

        miembro.trasladar(grupo2)
        miembro.refresh_from_db()
        self.assertTrue(miembro.grupo, grupo2)

    def test_resetear_contrasena_cedula(self):
        """Prueba que se cambie la contraseña del miembro a su cedula."""

        miembro = MiembroFactory(lider=True)
        miembro.usuario.set_password('password')

        miembro.resetear_contrasena()
        self.assertTrue(
            miembro.usuario.check_password(miembro.cedula),
            msg="La nueva contraseña deberia ser la identificación del miembro."
        )

    def test_resetear_contresena_envia_email(self):
        """Prueba que cuando se modifique la contraseña se notifique al miembro de esto por mail."""

        from django.core import mail

        miembro = MiembroFactory(lider=True)

        miembro.resetear_contrasena()
        self.assertEqual(len(mail.outbox), 1, msg="El outbox deberia contener un mensaje.")
        self.assertListEqual(mail.outbox[0].to, [miembro.email])
