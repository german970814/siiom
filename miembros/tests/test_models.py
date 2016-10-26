from common.tests.base import BaseTest
from grupos.models import Grupo
from grupos.tests.factories import GrupoFactory
from .factories import MiembroFactory


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

    def test_transladar_miembro_mismo_grupo(self):
        """
        Prueba que cuando se quiere transladar un miembro al mismo grupo no se cambie el grupo actual.
        """

        grupo = GrupoFactory()
        miembro = MiembroFactory(grupo=grupo)

        miembro.transladar(grupo)
        miembro.refresh_from_db()
        self.assertEqual(miembro.grupo, grupo)

    def test_transladar_miembro_mueve(self):
        """
        Prueba que se translada un miembro a un nuevo grupo.
        """

        grupo1 = GrupoFactory()
        grupo2 = GrupoFactory()
        miembro = MiembroFactory(grupo=grupo1)

        miembro.transladar(grupo2)
        miembro.refresh_from_db()
        self.assertTrue(miembro.grupo, grupo2)
