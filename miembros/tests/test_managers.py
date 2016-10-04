from django.test import TestCase
from grupos.tests.factories import GrupoFactory, RedFactory
from miembros.models import Miembro
from .factories import MiembroFactory


class MiembroManagerTest(TestCase):
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
