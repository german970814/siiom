from common.tests.base import BaseTest
from ..models import Grupo, HistorialEstado
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

        raiz_obtenida = Grupo.objects.raiz()
        self.assertEqual(raiz_obtenida, raiz)

    def test_no_hay_raiz_arbol_devuelva_none(self):
        """
        Prueba que si no hay grupo raiz en la iglesia en el arbol de grupos, devuelva None.
        """

        raiz_obtenida = Grupo.objects.raiz()
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

    def test_hojas_devuelve_grupos_sin_descendientes(self):
        """
        Verifica que hojas solo devuelva grupos que no tengan descendientes.
        """

        self.crear_arbol()
        queryset = Grupo.objects.hojas()

        self.assertNotIn(Grupo.objects.get(id=100), queryset)
        self.assertIn(Grupo.objects.get(id=200), queryset)
        self.assertNotIn(Grupo.objects.get(id=300), queryset)
        self.assertNotIn(Grupo.objects.get(id=400), queryset)
        self.assertNotIn(Grupo.objects.get(id=500), queryset)
        self.assertIn(Grupo.objects.get(id=600), queryset)
        self.assertIn(Grupo.objects.get(id=700), queryset)
        self.assertIn(Grupo.objects.get(id=800), queryset)

        g = Grupo.objects.get(id=700)
        g.actualizar_estado(estado=HistorialEstado.ARCHIVADO)

        self.assertIn(Grupo.objects.get(id=400), Grupo.objects.hojas())

    def test_archivados(self):
        """
        Prueba el queryset de archivados.
        """

        GrupoFactory()
        grupo = GrupoFactory()

        self.assertEqual(
            [],
            list(Grupo.objects.archivados().values_list('id', flat=1))
        )

        grupo.actualizar_estado(estado=HistorialEstado.ARCHIVADO)

        self.assertIn(grupo, Grupo.objects.archivados())
        self.assertNotIn(grupo, Grupo.objects.get_queryset()._archivados())

    def test_suspendidos(self):
        """
        Prueba el queryset de suspendidos.
        """

        GrupoFactory()
        grupo = GrupoFactory()

        self.assertEqual(
            [],
            list(Grupo.objects.suspendidos().values_list('id', flat=1))
        )

        grupo.actualizar_estado(estado=HistorialEstado.SUSPENDIDO)

        self.assertIn(grupo, Grupo.objects.suspendidos())
        self.assertNotIn(grupo, Grupo.objects.get_queryset()._suspendidos())

    def test_inactivos(self):
        """
        Prueba el queryset de inactivos.
        """

        GrupoFactory()
        grupo = GrupoFactory()

        self.assertEqual(
            [],
            list(Grupo.objects.inactivos().values_list('id', flat=1))
        )

        grupo.actualizar_estado(estado=HistorialEstado.INACTIVO)

        self.assertIn(grupo, Grupo.objects.inactivos())
        self.assertNotIn(grupo, Grupo.objects.get_queryset()._inactivos())

    def test_queryset_activos_solo_traiga_grupos_activos(self):
        """
        Prueba que los querysets de grupos activos solo traiga grupos activos
        """

        self.crear_arbol()
        padre = Grupo.objects.get(id=100)

        ids_grupos = Grupo.objects.activos().values_list('id', flat=1)

        for grupo in padre.grupos_red:
            self.assertIn(grupo.id, ids_grupos)

        grupo_a = Grupo.objects.get(id=600)
        grupo_a.actualizar_estado(estado=HistorialEstado.INACTIVO)

        self.assertNotIn(grupo_a, Grupo.objects.activos())

        grupo_b = Grupo.objects.get(id=500)
        grupo_b.actualizar_estado(estado=HistorialEstado.SUSPENDIDO)

        self.assertNotIn(grupo_b, Grupo.objects.activos())

        grupo_c = Grupo.objects.get(id=800)
        grupo_c.actualizar_estado(estado=HistorialEstado.ARCHIVADO)

        self.assertNotIn(grupo_c, Grupo.objects.activos())

    def test_grupos_archivados_not_in_queryset_objects(self):
        """
        Prueba que los grupos en estado archivado no esten saliendo en queryset de objects
        """

        import datetime
        self.crear_arbol()
        grupo = Grupo.objects.get(id=500)

        self.assertIn(grupo, Grupo.objects.all())

        grupo.actualizar_estado(
            estado=HistorialEstado.ARCHIVADO, fecha=grupo.fechaApertura + datetime.timedelta(weeks=5)
        )

        self.assertNotIn(grupo, Grupo.objects.all())
        self.assertIn(grupo, Grupo._objects.all())
