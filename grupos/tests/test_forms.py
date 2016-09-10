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
            'lider1': self.lider1.id, 'lider2': self.lider2.id, 'direccion': 'Calle 34 N 74 - 23', 'estado': 'A',
            'fechaApertura': '2012-03-03', 'diaGAR': '1', 'horaGAR': '12:00', 'diaDiscipulado': '3',
            'horaDiscipulado': '16:00', 'nombre': 'Pastor presidente', 'barrio': self.barrio.id
        }

        return data

    def test_lider1_lider2_solo_muestra_lideres(self):
        """
        Prueba que en los campos lider1 y lider2 solo se muestren miembros que sean lideres.
        """

        no_lider = MiembroFactory()
        form = GrupoRaizForm()

        self.assertNotIn(no_lider, form.fields['lider1'].queryset)
        self.assertNotIn(no_lider, form.fields['lider2'].queryset)

    def test_lider1_lider2_solo_muestra_lideres_sin_grupo(self):
        """
        Prueba que en los campos lider1 y lider2 solo se muestren miembros que sean lideres que no lideren grupo.
        """

        grupo = GrupoFactory()
        lider_sin_grupo = MiembroFactory(lider=True)
        form = GrupoRaizForm()

        self.assertNotIn(grupo.lider1, form.fields['lider1'].queryset)
        self.assertNotIn(grupo.lider1, form.fields['lider2'].queryset)

        self.assertIn(lider_sin_grupo, form.fields['lider1'].queryset)
        self.assertIn(lider_sin_grupo, form.fields['lider2'].queryset)

    def test_lider1_lider2_muestra_lideres_grupo_raiz(self):
        """
        Prueba que en los campos lider1 y lider2 muestren los lideres del grupo raiz.
        """

        raiz = GrupoRaizFactory(con_lider2=True)
        form = GrupoRaizForm(instance=raiz)

        self.assertIn(raiz.lider1, form.fields['lider1'].queryset)
        self.assertIn(raiz.lider2, form.fields['lider2'].queryset)

    def test_form_valido_si_datos_no_requeridos_vacios(self):
        """
        Prueba que el formulario sea valido aunque los campos lider2, dia discipulado y hora discipulado esten vacíos.
        """

        data = self.datos_formulario()
        data.pop('lider2')
        data.pop('diaDiscipulado')
        data.pop('horaDiscipulado')

        form = GrupoRaizForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_no_valido_si_datos_requeridos_vacios(self):
        """
        Prueba que el formulario sea invalido si falta alguno de los siguientes campos: lider1, direccion, estado,
        fechaApertura, diaGAR, horaGAR, nombre, barrio.
        """

        data = self.datos_formulario()
        data.pop('lider1')
        data.pop('estado')
        data.pop('diaGAR')
        data.pop('barrio')
        data.pop('nombre')
        data.pop('horaGAR')
        data.pop('direccion')
        data.pop('fechaApertura')

        form = GrupoRaizForm(data=data)
        self.assertFalse(form.is_valid())
