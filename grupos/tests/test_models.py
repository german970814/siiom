from grupos.models import Grupo
from .base import GruposBaseTest


class GrupoModelTest(GruposBaseTest):
    """
    Pruebas unitarias para el modelo Grupo.
    """

    def test_obtener_arbol_no_hay_raiz_devuelve_lista_vacio(self):
        """
        Prueba que si no existe raiz en el arbol de grupos, devuelva una lista vacía.
        """

        Grupo.objects.all().delete()
        lista_obtenida = Grupo.obtener_arbol()
        self.assertListEqual(lista_obtenida, [])

    def test_obtener_arbol_completo(self):
        """
        Prueba que la lista obtenida sea igual a la lista del arbol completo.
        """

        lista_obtenida = Grupo.obtener_arbol()
        self.assertListEqual(lista_obtenida, self.lista_arbol_completo)

    def test_obtener_arbol_padre_especifico(self):
        """
        Prueba que la lista obtenida sea igual a la lista del arbol de un padre especifico.
        """

        cb2 = Grupo.objects.get(id=3)
        lista_obtenida = Grupo.obtener_arbol(cb2)
        self.assertListEqual(lista_obtenida, self.lista_arbol_cb2)

    def test_transladar_grupo_mismo_padre(self):
        """
        Prueba que cuando se quiere transladar un grupo al mismo padre no se cambie el grupo padre.
        """

        grupo = Grupo.objects.get(id=5)
        padre = grupo.get_parent()

        grupo.transladar(padre)
        self.assertEqual(grupo.get_parent(), padre)

    def test_transladar_grupo_mueve_lideres_grupo_pertenecen(self):
        """
        Prueba que cuando se translada un grupo a un nuevo padre, tambien se modifica el grupo al que pertenecen los
        lideres del grupo que se esta transladando.
        """

        grupo = Grupo.objects.get(id=5)
        nuevo_padre = Grupo.objects.get(id=8)

        grupo.transladar(nuevo_padre)
        self.assertTrue(all(lider.grupo == nuevo_padre for lider in grupo.lideres.all()))

    def test_transladar_grupo_red(self):
        """
        Prueba que cuando se translada un grupo a un nuevo padre que se encuentre en otra red, el grupo y todos
        sus descendientes se mueven a la nueva red.
        """

        grupo = Grupo.objects.get(id=5)
        nuevo_padre = Grupo.objects.get(id=2)
        red_actual = grupo.red

        grupo.transladar(nuevo_padre)
        grupo.refresh_from_db()
        self.assertEqual(grupo.red, nuevo_padre.red)
        self.assertTrue(all(descendiente.red == nuevo_padre.red for descendiente in grupo.get_descendants()))
