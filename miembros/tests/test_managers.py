from django.test import TestCase
from grupos.tests.factories import GrupoFactory
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

        lider_sin_grupo = MiembroFactory(lider=True)
        grupo = GrupoFactory()

        lideres = Miembro.objects.lideres_disponibles()
        self.assertIn(lider_sin_grupo, lideres)
        self.assertNotIn(grupo.lideres.first(), lideres)
