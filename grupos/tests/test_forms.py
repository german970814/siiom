from django.test import TestCase
from miembros.tests.factories import MiembroFactory, BarrioFactory
from grupos.tests.factories import GrupoFactory, GrupoRaizFactory
from grupos.forms import GrupoRaizForm
from grupos.models import Grupo


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
            'barrio': self.barrio.id, 'lideres': [self.lider1.id, self.lider2.id]
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

    def test_campo_lideres_muestra_lideres_del_grupo_raiz(self):
        """
        Prueba que en el campo lideres muestren los lideres del grupo raiz.
        """

        raiz = GrupoRaizFactory()
        form = GrupoRaizForm(instance=raiz)

        self.assertIn(raiz.lideres.first(), form.fields['lideres'].queryset)

    def test_formulario_crea_raiz_se_asigna_grupo_a_lideres_escogidos(self):
        """
        Prueba que cuando se guarde el formulario se crea el grupo raiz sino existe y es asignado a los lideres
        escogidos.
        """

        form = GrupoRaizForm(data=self.datos_formulario())
        raiz = form.save()
        self.lider1.refresh_from_db()
        self.lider2.refresh_from_db()

        self.assertEqual(len(Grupo.get_root_nodes()), 1)
        self.assertEqual(self.lider1.grupo_lidera, raiz)
        self.assertEqual(self.lider2.grupo_lidera, raiz)

    def test_formulario_no_crea_nueva_raiz_si_ya_existe(self):
        """
        Prueba que cuando se guarde el formulario no se cree un nuevo grupo raiz si ya existe.
        """

        raiz = GrupoRaizFactory()
        form = GrupoRaizForm(instance=raiz, data=self.datos_formulario())
        form.save()

        self.assertEqual(len(Grupo.get_root_nodes()), 1)

    def test_modificar_lideres_raiz(self):
        """
        Prueba que cuando se editen los lideres del grupo raiz, se les coloque a los lideres nuevos el grupo raiz como
        su grupo que lidera y a los lideres que se cambiaron se les quite.
        """

        raiz = GrupoRaizFactory()
        lider3 = MiembroFactory(lider=True, grupo_lidera=raiz)
        lideres_viejos = list(raiz.lideres.values_list('id', flat=True))

        data = self.datos_formulario()
        data['lideres'].append(lider3.id)
        form = GrupoRaizForm(instance=raiz, data=data)
        form.save()

        lider3.refresh_from_db()
        self.lider1.refresh_from_db()
        self.lider2.refresh_from_db()
        self.assertEqual(lider3.grupo_lidera, raiz)
        self.assertEqual(self.lider1.grupo_lidera, raiz)
        self.assertEqual(self.lider2.grupo_lidera, raiz)
        self.assertEqual(len(raiz.lideres.filter(id__in=lideres_viejos)), 1)
