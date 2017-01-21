from miembros.tests.factories import MiembroFactory
from common.tests.base import BaseTest
from ..models import Grupo
from .factories import ReunionGARFactory, ReunionDiscipuladoFactory


class GrupoModelTest(BaseTest):
    """
    Pruebas unitarias para el modelo Grupo.
    """

    def setUp(self):
        self.crear_arbol()

    def test_obtener_arbol_no_hay_raiz_devuelve_lista_vacio(self):
        """
        Prueba que si no existe raiz en el arbol de grupos, devuelva una lista vacía.
        """

        Grupo.objects.all().delete()
        lista_obtenida = Grupo.obtener_arbol()
        self.assertListEqual(lista_obtenida, [])

    def test_obtener_arbol_completo_sin_especificar_iglesia_devuelve_vacio(self):
        """
        Prueba que se obtenga una lista vacia si se intenta obtener el arbol completo sin indicar una iglesia.
        """

        lista_obtenida = Grupo.obtener_arbol()
        self.assertListEqual(lista_obtenida, [])

    def test_obtener_arbol_completo(self):
        """
        Prueba que la lista obtenida sea igual a la lista del arbol completo.
        """

        lista_obtenida = Grupo.obtener_arbol(iglesia=Grupo.objects.first().iglesia_id)
        self.assertListEqual(lista_obtenida, self.lista_arbol_completo)

    def test_obtener_arbol_padre_especifico(self):
        """
        Prueba que la lista obtenida sea igual a la lista del arbol de un padre especifico.
        """

        cb2 = Grupo.objects.get(id=300)
        lista_obtenida = Grupo.obtener_arbol(cb2)
        self.assertListEqual(lista_obtenida, self.lista_arbol_cb2)

    def test_obtener_ruta(self):
        """
        Prueba que la lista obtenida sea igual a la lista de ruta.
        """

        ruta = Grupo.objects.filter(id__in=[300, 500, 600]).order_by('id')
        ruta_obtenida = Grupo.obtener_ruta(ruta[0], ruta[2])

        self.assertListEqual(ruta_obtenida, list(ruta))

    def test_transladar_grupo_mismo_padre(self):
        """
        Prueba que cuando se quiere transladar un grupo al mismo padre no se cambie el grupo padre.
        """

        grupo = Grupo.objects.get(id=500)
        padre = grupo.get_parent()

        grupo.transladar(padre)
        self.assertEqual(grupo.get_parent(), padre)

    def test_transladar_grupo_mueve_lideres_grupo_pertenecen(self):
        """
        Prueba que cuando se translada un grupo a un nuevo padre, tambien se modifica el grupo al que pertenecen los
        lideres del grupo que se esta transladando.
        """

        grupo = Grupo.objects.get(id=500)
        nuevo_padre = Grupo.objects.get(id=800)

        grupo.transladar(nuevo_padre)
        self.assertTrue(all(lider.grupo == nuevo_padre for lider in grupo.lideres.all()))

    def test_transladar_grupo_red(self):
        """
        Prueba que cuando se translada un grupo a un nuevo padre que se encuentre en otra red, el grupo y todos
        sus descendientes se mueven a la nueva red.
        """

        grupo = Grupo.objects.get(id=500)
        nuevo_padre = Grupo.objects.get(id=200)

        grupo.transladar(nuevo_padre)
        grupo.refresh_from_db()
        self.assertEqual(grupo.red, nuevo_padre.red)
        self.assertTrue(all(descendiente.red == nuevo_padre.red for descendiente in grupo.get_descendants()))

    def test_discipulos_devuelve_solo_miembros_grupo_son_lideres(self):
        """
        Prueba que los discipulos obtenidos son los miembros del grupo que son lideres.
        """

        grupo = Grupo.objects.get(id=300)
        miembro = MiembroFactory(grupo=grupo)
        lider = Grupo.objects.get(id=500).lideres.first()
        otro_lider = Grupo.objects.get(id=200).lideres.first()

        discipulos = list(grupo.discipulos)

        self.assertIn(lider, discipulos)
        self.assertNotIn(miembro, discipulos)
        self.assertNotIn(otro_lider, discipulos)

    def test_reunion_GAR_sin_ofrenda_confirmada(self):
        """
        Prueba que devuelva las reuniones GAR a las cuales no se les haya confirmado la ofrenda.
        """

        grupo = Grupo.objects.get(id=200)
        confirmada = ReunionGARFactory(grupo=grupo, confirmacionEntregaOfrenda=True)
        no_confirmada = ReunionGARFactory(grupo=grupo, confirmacionEntregaOfrenda=False)

        reuniones = grupo.reuniones_GAR_sin_ofrenda_confirmada
        self.assertIn(no_confirmada, reuniones)
        self.assertNotIn(confirmada, reuniones)

    def test_confirmar_ofrenda_GAR(self):
        """
        Prueba que se confirmen la ofrenda de las reuniones GAR ingresadas.
        """

        grupo = Grupo.objects.get(id=200)
        no_confirmada1 = ReunionGARFactory(grupo=grupo)
        no_confirmada2 = ReunionGARFactory(grupo=grupo)

        grupo.confirmar_ofrenda_reuniones_GAR([no_confirmada1.id])
        no_confirmada1.refresh_from_db()
        no_confirmada2.refresh_from_db()

        self.assertTrue(no_confirmada1.confirmacionEntregaOfrenda)
        self.assertFalse(no_confirmada2.confirmacionEntregaOfrenda)

    def test_reunion_discipulado_sin_ofrenda_confirmada(self):
        """
        Prueba que devuelva las reuniones de discipulado a las cuales no se les haya confirmado la ofrenda.
        """

        grupo = Grupo.objects.get(id=200)
        confirmada = ReunionDiscipuladoFactory(grupo=grupo, confirmacionEntregaOfrenda=True)
        no_confirmada = ReunionDiscipuladoFactory(grupo=grupo, confirmacionEntregaOfrenda=False)

        reuniones = grupo.reuniones_discipulado_sin_ofrenda_confirmada
        self.assertIn(no_confirmada, reuniones)
        self.assertNotIn(confirmada, reuniones)

    def test_confirmar_ofrenda_discipulado(self):
        """
        Prueba que se confirmen la ofrenda de las reuniones de discipulado ingresadas.
        """

        grupo = Grupo.objects.get(id=200)
        no_confirmada1 = ReunionDiscipuladoFactory(grupo=grupo)
        no_confirmada2 = ReunionDiscipuladoFactory(grupo=grupo)

        grupo.confirmar_ofrenda_reuniones_discipulado([no_confirmada1.id])
        no_confirmada1.refresh_from_db()
        no_confirmada2.refresh_from_db()

        self.assertTrue(no_confirmada1.confirmacionEntregaOfrenda)
        self.assertFalse(no_confirmada2.confirmacionEntregaOfrenda)

    def test_grupos_red(self):
        """
        Prueba que devuelva los grupos de la red del grupo escogido.
        """

        grupo = Grupo.objects.get(id=500)
        red = grupo.grupos_red

        self.assertEqual(grupo, red[0])
        self.assertEqual(600, red[1].id)

    def test_obtener_cabeza_de_red(self):
        """
        Prueba que devuelva la cabeza de red del grupo indicado.
        """

        grupo = Grupo.objects.get(id=600)

        cabeza = grupo.cabeza_red
        self.assertEqual(cabeza.pk, 500, msg="El grupo cabeza de red no esta correcto.")

    def test_obtener_cabeza_de_red_retorna_none(self):
        """
        Prueba que devuelva NONE como cabeza de red si el grupo se encuentra por encima de los 72 del inicio del arbol.
        """

        grupo = Grupo.objects.get(id=200)
        self.assertIsNone(grupo.cabeza_red)
