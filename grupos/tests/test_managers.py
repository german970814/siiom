from common.tests.base import BaseTest
from iglesias.tests.factories import IglesiaFactory
from ..models import Grupo
from .factories import GrupoRaizFactory, GrupoFactory, RedFactory, ReunionGARFactory, ReunionDiscipuladoFactory


class GrupoManagerTest(BaseTest):
    """
    Pruebas unitarias para el manager de grupos.
    """

    def test_obtener_raiz_arbol(self):
        """
        Prueba que el grupo obtenido sea la raiz del arbol.
        """

        raiz = GrupoRaizFactory()
        GrupoFactory(parent=raiz)

        raiz_obtenida = Grupo.objects.raiz(raiz.iglesia_id)
        self.assertEqual(raiz_obtenida, raiz)

    def test_no_hay_raiz_iglesia_ingresada_arbol_devuelva_none(self):
        """
        Prueba que si no hay grupo raiz en la iglesia ingresada en el arbol de grupos, devuelva None.
        """

        GrupoRaizFactory(iglesia__nombre='otra iglesia')

        raiz_obtenida = Grupo.objects.raiz(IglesiaFactory())
        self.assertIsNone(raiz_obtenida)

    def test_red_devuelve_grupos_correctos(self):
        """
        Prueba que los grupos obtenidos pertenezcan a la red ingresada.
        """

        red_jovenes = RedFactory()
        grupo_jovenes = GrupoFactory()
        otra_red = RedFactory(nombre='adultos')
        otro_grupo = GrupoFactory(red=otra_red)

        grupos = Grupo.objects.red(red_jovenes)

        self.assertIn(grupo_jovenes, grupos)
        self.assertNotIn(otro_grupo, grupos)

    def test_devuelve_grupo_sin_confirmar_ofrenda_GAR(self):
        """
        Prueba que devuelve el grupo que falta por confirmar ofrenda reunion GAR.
        """

        sin_confirmar = ReunionGARFactory()
        confirmada = ReunionGARFactory(confirmacionEntregaOfrenda=True)

        grupos = Grupo.objects.sin_confirmar_ofrenda_GAR()

        self.assertIn(sin_confirmar.grupo, grupos)
        self.assertNotIn(confirmada.grupo, grupos)

    def test_devuelve_grupo_sin_confirmar_ofrenda_GAR_una_sola_vez(self):
        """
        Prueba que devuleva el grupos que falta por confirmar ofrenda reunión GAR una sola vez aunque deba confirmar
        mas de una ofrenda.
        """

        sin_confirmar = ReunionGARFactory()
        ReunionGARFactory(grupo=sin_confirmar.grupo)

        grupos = Grupo.objects.sin_confirmar_ofrenda_GAR()

        self.assertEqual(grupos.count(), 1)

    def test_devuelve_grupo_sin_confirmar_ofrenda_discipulado(self):
        """
        Prueba que devuelve el grupo que falta por confirmar ofrenda reunion discipulado.
        """

        sin_confirmar = ReunionDiscipuladoFactory()
        confirmada = ReunionDiscipuladoFactory(confirmacionEntregaOfrenda=True)

        grupos = Grupo.objects.sin_confirmar_ofrenda_discipulado()

        self.assertIn(sin_confirmar.grupo, grupos)
        self.assertNotIn(confirmada.grupo, grupos)

    def test_devuelve_grupo_sin_confirmar_ofrenda_discipulado_una_sola_vez(self):
        """
        Prueba que devuleva el grupos que falta por confirmar ofrenda reunión discipulado una sola vez aunque deba
        confirmar mas de una ofrenda.
        """

        sin_confirmar = ReunionDiscipuladoFactory()
        ReunionDiscipuladoFactory(grupo=sin_confirmar.grupo)

        grupos = Grupo.objects.sin_confirmar_ofrenda_discipulado()

        self.assertEqual(grupos.count(), 1)
