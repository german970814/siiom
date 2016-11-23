from django.test import TestCase
from grupos import utils, managers


class UtilsModuleTest(TestCase):
    """
    Pruebas unitarias para el modulo Utils.
    """

    def test_convertir_lista_queryset(self):
        """
        Prueba cuando se ingresa una lista de grupos, la función devuelva un queryset.
        """

        queryset = utils.convertir_lista_a_queryset([])
        self.assertIsInstance(queryset, managers.GrupoQuerySet)