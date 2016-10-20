from common.tests.base import BaseTest
from grupos.models import Grupo


class MiembroModelTest(BaseTest):
    """
    Pruebas unitarias para el modelo Miembro.
    """

    def test_es_director_red(self):
        """
        Prueba que si el miembro es director de red devuelva True.
        """

        self.crear_arbol()
        director = Grupo.objects.get(id=200).lideres.first()
        no_director = Grupo.objects.get(id=500).lideres.first()

        self.assertTrue(director.es_director_red)
        self.assertFalse(no_director.es_director_red)
