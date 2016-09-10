from django.test import TestCase
from grupos.models import Grupo
from grupos.tests.factories import GrupoFactory
from .factories import MiembroFactory


class MiembroManagerTest(TestCase):
    """
    Pruebas unitarias para el manager de miembros.
    """

    def test_lideres_disponibles(self):
        """
        Los lideres disponibles son aquellos que no se encuentran liderando grupo.
        """

        lider_sin_grupo = MiembroFactory(lider=True)
        grupo = GrupoFactory(con_lider2=True)

        lideres = Grupo.objects.lideres_disponibles()
        self.assertIn(lider_sin_grupo, lideres)
        self.assertNotIn(grupo.lider1, lideres)
        self.assertNotIn(grupo.lider2, lideres)
