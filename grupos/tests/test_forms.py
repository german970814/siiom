from django.test import TestCase
from miembros.tests.factories import MiembroFactory, BarrioFactory
from grupos.tests.factories import GrupoFactory, GrupoRaizFactory
from grupos.forms import GrupoRaizForm


class GrupoRaizFormTest(TestCase):
    """
    Pruebas unitarias para el formulario de creación y/o edición del grupo raiz.
    """

    def setUp(self):
        self.lider1 = MiembroFactory(lider=True)
        self.lider2 = MiembroFactory(lider=True)
        self.barrio = BarrioFactory()

    def datos_formulario(self):
        """
        Retorna un diccionario con datos para el formulario GrupoRaiz.
        """

        data = {
            'direccion': 'Calle 34 N 74 - 23', 'estado': 'A', 'fechaApertura': '2012-03-03', 'diaGAR': '1',
            'horaGAR': '12:00', 'diaDiscipulado': '3', 'horaDiscipulado': '16:00', 'nombre': 'Pastor presidente',
            'barrio': self.barrio.id, 'lideres': self.lider1.id
        }

        return data

    def test_campo_lideres_solo_muestra_lideres(self):
        """
        Prueba que el campo lideres solo se muestren miembros que sean lideres.
        """

        no_lider = MiembroFactory()
        form = GrupoRaizForm()

        self.assertNotIn(no_lider, form.fields['lideres'].queryset)

    def test_campo_lideres_solo_muestra_lideres_sin_grupo(self):
        """
        Prueba que en el campo lideres solo se muestren miembros que sean lideres que no lideren grupo.
        """

        grupo = GrupoFactory()
        lider_sin_grupo = MiembroFactory(lider=True)
        form = GrupoRaizForm()

        self.assertNotIn(grupo.lideres.first(), form.fields['lideres'].queryset)
        self.assertIn(lider_sin_grupo, form.fields['lideres'].queryset)

    def test_campo_lideres_muestra_lideres_grupo_raiz(self):
        """
        Prueba que en el campo lideres muestren los lideres del grupo raiz.
        """

        raiz = GrupoRaizFactory()
        form = GrupoRaizForm(instance=raiz)

        self.assertIn(raiz.lideres.first(), form.fields['lideres'].queryset)
