from common.tests.base import BaseTestAPI
from .factories import GrupoFactory


class LideresGrupoTest(BaseTestAPI):
    """
    Pruebas unitarias para la vista lideres de un grupo.
    """

    def test_get_lideres_grupo(self):
        """
        Prueba que me devuelva solo los lideres del grupo ingresado.
        """

        grupo = GrupoFactory()
        self.url = self.reverse('grupos:lideres_api', grupo.pk)
        response = self.GET()

        self.assertEqual(grupo.lideres.first().pk, response[0]['pk'])
