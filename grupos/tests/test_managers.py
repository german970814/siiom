import datetime
from freezegun import freeze_time
from django.test import tag
from common.tests.base import BaseTest
from ..models import Grupo, HistorialEstado, ReunionGAR
from .factories import (
    GrupoRaizFactory, GrupoFactory, RedFactory, ReunionGARFactory, ReunionDiscipuladoFactory, HistorialEstadoFactory
)


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

        self.crear_arbol()
        grupo = Grupo.objects.get(id=500)

        self.assertIn(grupo, Grupo.objects.all())

        grupo.actualizar_estado(
            estado=HistorialEstado.ARCHIVADO, fecha=grupo.fechaApertura + datetime.timedelta(weeks=5)
        )

        self.assertNotIn(grupo, Grupo.objects.all())
        self.assertIn(grupo, Grupo._objects.all())

    def test_declarar_vacaciones_crea_reuniones_como_realizada(self):
        """Prueba que cuando se declaren los grupos en vacaciones se coloquen las reuniones en las fechas escogidas como
        que no realizo grupo."""

        with freeze_time("2017-12-15"):
            now = datetime.datetime.now()
            grupo1 = GrupoFactory(fechaApertura=now, historial__fecha=now)
        with freeze_time("2017-12-18"):
            dic_18 = datetime.date.today()
        with freeze_time("2017-12-31"):
            dic_31 = datetime.date.today()
        
        Grupo.objects.declarar_vacaciones(dic_18, dic_31)
        self.assertFalse(
            all([r.realizada for r in grupo1.reuniones_gar.all()]),
            msg="Las reuniones debieron ser creadas como no realizadas."
        )

    def test_declarar_vacaciones_crea_todas_reuniones_dentro_rango_fechas(self):
        """
        Prueba que cuando se declaren los grupos en vacaciones se coloquen todas las reuniones dentro del rango de
        fechas dadas.
        """

        with freeze_time("2017-12-15"):
            now = datetime.datetime.now()
            grupo1 = GrupoFactory(fechaApertura=now, historial__fecha=now)
        
        with freeze_time("2017-12-18"):
            dic_18 = datetime.date.today()
        with freeze_time("2017-12-31"):
            dic_31 = datetime.date.today()
        
        Grupo.objects.declarar_vacaciones(dic_18, dic_31)
        self.assertEqual(
            grupo1.reuniones_gar.count(), 2,
            msg="Debido al que el rango de fechas son dos semanas, solo deben haber reuniones."
        )
    
    def test_declarar_vacaciones_solo_grupos_activos(self):
        """
        Prueba que solo se creen reuniones para grupos activos.
        """

        with freeze_time("2017-12-13"):
            now = datetime.datetime.now()
            grupo1 = GrupoFactory(fechaApertura=now)
            grupo2 = GrupoFactory(fechaApertura=now)
            grupo3 = GrupoFactory(fechaApertura=now)
        
        with freeze_time("2017-12-14"):
            grupo1.actualizar_estado('IN')
            grupo2.actualizar_estado('SU')
            grupo3.actualizar_estado('AR')
        
        with freeze_time("2017-12-18"):
            dic_18 = datetime.date.today()
        with freeze_time("2017-12-31"):
            dic_31 = datetime.date.today()
        
        Grupo.objects.declarar_vacaciones(dic_18, dic_31)
        self.assertEqual(ReunionGAR.objects.count(), 0, msg="No debe haber ninguna reunion creada")
    
    def test_declarar_vacaciones_no_cree_reporte_si_grupo_ya_reporto(self):
        """
        Prueba que no se cree un reporte si el grupo ya reporto.
        """

        with freeze_time("2017-12-13"):
            grupo = GrupoFactory(fechaApertura=datetime.datetime.now())
        
        with freeze_time("2017-12-20"):
            reunion = ReunionGARFactory(grupo=grupo, fecha=datetime.datetime.now())
        
        with freeze_time("2017-12-18"):
            dic_18 = datetime.date.today()
        with freeze_time("2017-12-31"):
            dic_31 = datetime.date.today()
        
        Grupo.objects.declarar_vacaciones(dic_18, dic_31)
        self.assertEqual(ReunionGAR.objects.exclude(id=reunion.id).count(), 1, msg="Solo se debio crear una sola reunion")

    def test_devuelve_grupo_sin_reportar_reunion_GAR(self):
        """Prueba que devuelva el grupo que no ha reportado reunion GAR en el rango de fecha ingresado."""

        grupo = GrupoFactory()        
        with freeze_time("2018-01-01"):
            ene_01 = datetime.date.today()
        with freeze_time("2018-01-07"):
            ene_07 = datetime.date.today()

        grupos = Grupo.objects.sin_reportar_reunion_GAR(ene_01, ene_07)
        self.assertTrue(
            grupos.filter(id=grupo.id).exists(),
            msg="El grupo {0} no ha reportado reunion por lo tanto debe ser True.".format(grupo.id)
        )

    def test_no_devuelve_grupo_que_reporto_reunion_GAR(self):
        """Prueba que no devuelva el grupo que reporto reunion GAR en el rango de fecha ingresado."""

        GrupoFactory()
        grupo = GrupoFactory()
        with freeze_time("2018-01-03"):
            reunion = ReunionGARFactory(fecha=datetime.date.today(), grupo=grupo)
        
        with freeze_time("2018-01-01"):
            ene_01 = datetime.date.today()
        with freeze_time("2018-01-07"):
            ene_07 = datetime.date.today()

        grupos = Grupo.objects.sin_reportar_reunion_GAR(ene_01, ene_07)
        self.assertFalse(
            grupos.filter(id=grupo.id).exists(),
            msg="El grupo {0} ya reporto reunion por lo tanto debe ser False.".format(grupo.id)
        )

    def test_sin_reportar_reunion_GAR_no_devuelva_grupos_si_no_hay_grupos_activos(self):
        """Prueba que no devuelva ningún grupo si no hay grupos activos."""

        with freeze_time("2017-12-13"):
            now = datetime.datetime.now()
            grupo1 = GrupoFactory(fechaApertura=now)
            grupo2 = GrupoFactory(fechaApertura=now)
            grupo3 = GrupoFactory(fechaApertura=now)
        
        with freeze_time("2017-12-14"):
            grupo1.actualizar_estado('IN')
            grupo2.actualizar_estado('SU')
            grupo3.actualizar_estado('AR')
        
        with freeze_time("2018-01-01"):
            ene_01 = datetime.date.today()
        with freeze_time("2018-01-07"):
            ene_07 = datetime.date.today()


        grupos = Grupo.objects.sin_reportar_reunion_GAR(ene_01, ene_07)
        self.assertEqual(grupos.count(), 0)
    
    def test_pueden_reportar_discipulado_devuelve_grupos_con_hijos(self):
        """Prueba que me devuelva grupos que tengan por lo menos un hijo."""

        self.crear_arbol()
        
        grupos = Grupo.objects.pueden_reportar_discipulado()
        self.assertIn(Grupo.objects.get(id=100), grupos)
        self.assertIn(Grupo.objects.get(id=500), grupos)
    
    def test_pueden_reportar_discipulado_no_devuelve_grupos_sin_hijos(self):
        """Prueba que no devuelva grupos que no tengan hijos."""

        self.crear_arbol()

        grupos = Grupo.objects.pueden_reportar_discipulado()
        self.assertNotIn(Grupo.objects.get(id=700), grupos)
    
    def test_pueden_reportar_discipulado_no_devuelve_grupos_suspendidos(self):
        """Prueba que no devuelva grupos que tengan hijos pero que se encuentran en estado suspendido."""

        self.crear_arbol()
        suspendido = Grupo.objects.get(id=500)
        suspendido.actualizar_estado(estado=HistorialEstado.SUSPENDIDO)

        grupos = Grupo.objects.pueden_reportar_discipulado()
        self.assertNotIn(suspendido, grupos)
    
    def test_pueden_reportar_discipulado_no_duvuelve_grupos_con_un_solo_hijo_archivado(self):
        """Prueba que no devuelva grupos que tengan un solo hijo y este se encuentre archivado."""

        self.crear_arbol()
        Grupo.objects.get(id=700).actualizar_estado(estado=HistorialEstado.ARCHIVADO)

        grupos = Grupo.objects.pueden_reportar_discipulado()
        self.assertNotIn(Grupo.objects.get(id=400), grupos)
