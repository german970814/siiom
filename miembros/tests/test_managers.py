from unittest import mock
from common.tests.base import BaseTest
from grupos.tests.factories import GrupoFactory, RedFactory, GrupoHijoFactory
from ..models import Miembro
from .factories import MiembroFactory


class MiembroManagerTest(BaseTest):
    """
    Pruebas unitarias para el manager de miembros.
    """

    def test_lideres_disponibles(self):
        """
        Los lideres disponibles son aquellos que no se encuentran liderando grupo.
        """

        grupo = GrupoFactory()
        grupo2 = GrupoFactory()
        lider_sin_grupo = MiembroFactory(lider=True)
        lider_grupo = MiembroFactory(lider=True)
        lider_grupo.grupo_lidera = grupo
        lider_grupo.save()

        lideres_disponibles = Miembro.objects.lideres_disponibles()
        self.assertIn(lider_sin_grupo, lideres_disponibles)
        self.assertFalse(all(lider in lideres_disponibles for lider in grupo.lideres.all()))
        self.assertFalse(all(lider in lideres_disponibles for lider in grupo2.lideres.all()))

    def test_red_devuelve_miembros_correctos(self):
        """
        Prueba que los miembros obtenidos pertenezcan a la red ingresada.
        """

        red_jovenes = RedFactory()
        grupo_jovenes = GrupoFactory()
        miembro_jovenes = MiembroFactory(grupo=grupo_jovenes)
        otra_red = RedFactory(nombre='adultos')
        otro_grupo = GrupoFactory(red=otra_red)
        otro_miembro = MiembroFactory(grupo=otro_grupo)

        miembros = Miembro.objects.red(red_jovenes)

        self.assertIn(miembro_jovenes, miembros)
        self.assertNotIn(otro_miembro, miembros)

    def test_lideres_devuelve_los_miembros_iglesia_son_lideres(self):
        """
        Los lideres son los miembros de una iglesia que tengan el permiso de lider.
        """

        miembro = MiembroFactory()
        lider = MiembroFactory(lider=True)

        lideres = list(Miembro.objects.lideres2())
        self.assertIn(lider, lideres)
        self.assertNotIn(miembro, lideres)

    def test_lideres_red(self):
        """
        Prueba que los miembros obtenidos lideren grupo y pertenezcan a la red ingresada.
        """

        from grupos.models import Grupo

        self.crear_arbol()
        grupo = Grupo.objects.get(id=300)
        otro_grupo = Grupo.objects.get(id=200)
        miembro = MiembroFactory(lider=True, grupo=grupo)

        lideres = Miembro.objects.lideres_red(grupo.red)

        self.assertNotIn(miembro, lideres)
        self.assertIn(grupo.lideres.first(), lideres)
        self.assertNotIn(otro_grupo.lideres.first(), lideres)

    def test_trasladar_lideres_espera_lideres_sea_queryset(self):
        """
        Prueba que se levante una excepción si el parametro lideres no es un queryset.
        """

        grupo = GrupoFactory()
        with self.assertRaises(TypeError):
            Miembro.objects.trasladar_lideres([], grupo)
            Miembro.objects.trasladar_lideres(MiembroFactory(), grupo)

    def test_trasladar_lideres_espera_lideres_lideren_grupo(self):
        """
        Prueba que se levante una excepción si los lideres ingresados no lideran grupo.
        """

        grupo = GrupoFactory()
        lider = MiembroFactory(lider=True)
        miembro = MiembroFactory()

        with self.assertRaises(ValueError):
            lideres = Miembro.objects.filter(id__in=[lider.pk, miembro.pk])
            Miembro.objects.trasladar_lideres(lideres, grupo)

    def test_trasladar_lideres_mueve_lideres_al_nuevo_grupo(self):
        """
        Prueba que se trasladen los lideres al nuevo grupo.
        """

        padre = GrupoFactory()
        nuevo_grupo = GrupoFactory()
        grupo = GrupoHijoFactory(parent=padre)
        miembro = MiembroFactory(grupo_lidera=grupo, grupo=padre)

        Miembro.objects.trasladar_lideres(Miembro.objects.filter(id=miembro.pk), nuevo_grupo)
        miembro.refresh_from_db()
        self.assertEqual(miembro.grupo_lidera, nuevo_grupo)
        self.assertEqual(miembro.grupo, nuevo_grupo.get_parent())

    def test_trasladar_lideres_no_fusiona_grupos(self):
        """
        Prueba que si no se trasladan todos los lideres de un grupo al nuevo grupo, el grupo actual no se fusione con
        el nuevo grupo.
        """

        from grupos.models import Grupo

        padre = GrupoFactory()
        nuevo_grupo = GrupoFactory()
        grupo = GrupoHijoFactory(parent=padre)
        miembro = MiembroFactory(grupo_lidera=grupo, grupo=padre)

        Miembro.objects.trasladar_lideres(Miembro.objects.filter(id=miembro.pk), nuevo_grupo)
        self.assertEqual(grupo.lideres.count(), 1, msg="El grupo debio quedar con un lider.")
        self.assertIsNotNone(Grupo.objects.filter(pk=grupo.pk).exists())

    @mock.patch('grupos.models.Grupo.fusionar')
    def test_trasladar_lideres_fusiona_grupos(self, fusionar_mock):
        """
        Prueba que si se van a trasladan todos los lideres de un grupo a un nuevo grupo, el grupo actual se fusione con
        el nuevo grupo.
        """

        grupo = GrupoFactory()
        nuevo_grupo = GrupoFactory()
        MiembroFactory(grupo_lidera=grupo)

        Miembro.objects.trasladar_lideres(grupo.lideres.all(), nuevo_grupo)
        fusionar_mock.assert_called_once_with(nuevo_grupo)

    @mock.patch('grupos.models.Grupo.fusionar')
    def test_trasladar_lideres_fusiona_todos_los_grupos_si_mas_de_un_grupo(self, fusionar_mock):
        """
        Prueba que si los lideres a trasladar lideran mas de un grupo y los grupos se quedan sin lideres estos se
        fusionen con el nuevo grupo.
        """

        grupo1 = GrupoFactory()
        grupo2 = GrupoFactory()
        nuevo_grupo = GrupoFactory()

        lideres = Miembro.objects.filter(grupo_lidera__in=[grupo1.id, grupo2.id])
        Miembro.objects.trasladar_lideres(lideres, nuevo_grupo)
        self.assertEqual(fusionar_mock.call_count, 2, msg="Fusionar se debio ejecutar 2 veces porque eran 2 grupos.")
