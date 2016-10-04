from unittest import mock
from django.test import TestCase
from django.db import IntegrityError
from miembros.tests.factories import MiembroFactory, BarrioFactory
from grupos.tests.factories import GrupoFactory, GrupoRaizFactory, RedFactory
from grupos.forms import GrupoRaizForm, NuevoGrupoForm
from grupos.models import Grupo, Red
from .base import GruposBaseTest


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

    @mock.patch('django.db.models.query.QuerySet.update', side_effect=IntegrityError)
    def test_error_al_guardar_formulario_no_se_guarda_nada_en_db(self, update_mock):
        """
        Prueba que si ocurre un error al guardar el formulario no se guarde ni el grupo ni los lideres.
        """

        form = GrupoRaizForm(data=self.datos_formulario())
        form.save()
        self.lider1.refresh_from_db()
        self.lider2.refresh_from_db()

        self.assertTrue(update_mock.called)
        self.assertEqual(len(Grupo.get_root_nodes()), 0)
        self.assertEqual(self.lider1.grupo_lidera, None)
        self.assertEqual(self.lider2.grupo_lidera, None)

    @mock.patch('django.db.models.query.QuerySet.update', side_effect=IntegrityError)
    def test_error_al_guardar_formulario_agrega_error_form(self, update_mock):
        """
        Prueba que si ocurre un error al momento de guardar el formulario, se agregue un error al formulario.
        """

        form = GrupoRaizForm(data=self.datos_formulario())
        form.save()

        self.assertTrue(update_mock.called)
        self.assertEqual(len(form.non_field_errors()), 1)


class NuevoGrupoFormTest(GruposBaseTest):
    """
    Pruebas unitarias para el formulario de creación de grupos de una iglesia.
    """

    def setUp(self):
        super(NuevoGrupoFormTest, self).setUp()
        self.red_jovenes = Red.objects.get(nombre='jovenes')

    def test_campo_parent_solo_muestra_grupos_red_ingresada(self):
        """
        Prueba que el campo parent solo muestra los grupos pertenecientes a la red ingresada.
        """

        raiz = Grupo.objects.get(id=1)
        grupo1 = Grupo.objects.get(id=3)
        grupo2 = Grupo.objects.get(id=4)

        form = NuevoGrupoForm(red=self.red_jovenes)

        self.assertIn(grupo1, form.fields['parent'].queryset)
        self.assertNotIn(grupo2, form.fields['parent'].queryset)
        self.assertNotIn(raiz, form.fields['parent'].queryset)

    def test_campo_parent_muestra_raiz_sino_red_no_tiene_grupos(self):
        """
        Prueba que el campo parent muestre el grupo raiz de la iglesia si la red ingresada no tiene ningún grupo.
        """

        raiz = Grupo.objects.get(id=1)
        otro = Grupo.objects.get(id=3)
        red_nueva = RedFactory(nombre='nueva red')

        form = NuevoGrupoForm(red=red_nueva)
        self.assertIn(raiz, form.fields['parent'].queryset)
        self.assertNotIn(otro, form.fields['parent'].queryset)

    def test_campo_lideres_solo_muestra_lideres(self):
        """
        Prueba que el campo lideres solo se muestren miembros que sean lideres.
        """

        no_lider = MiembroFactory()
        form = NuevoGrupoForm(red=self.red_jovenes)

        self.assertNotIn(no_lider, form.fields['lideres'].queryset)

    def test_campo_lideres_solo_muestra_lideres_sin_grupo(self):
        """
        Prueba que en el campo lideres solo se muestren miembros que sean lideres que no lideren grupo.
        """

        grupo = Grupo.objects.get(id=3)
        lider_sin_grupo = MiembroFactory(lider=True, grupo=grupo)
        form = NuevoGrupoForm(red=self.red_jovenes)

        self.assertNotIn(grupo.lideres.first(), form.fields['lideres'].queryset)
        self.assertIn(lider_sin_grupo, form.fields['lideres'].queryset)

    def test_campo_lideres_solo_muestra_lideres_red_ingresada(self):
        """
        Prueba que el campo lideres solo muestra lideres que pertenecen a los grupos de la red ingresada.
        """

        grupo1 = Grupo.objects.get(id=3)
        lider_joven = MiembroFactory(lider=True, grupo=grupo1)

        grupo2 = Grupo.objects.get(id=4)
        otro_lider = MiembroFactory(lider=True, grupo=grupo2)

        form = NuevoGrupoForm(red=self.red_jovenes)

        self.assertIn(lider_joven, form.fields['lideres'].queryset)
        self.assertNotIn(otro_lider, form.fields['lideres'].queryset)

    def test_campo_lideres_muestra_lideres_raiz_si_red_no_tiene_grupo(self):
        """
        Prueba que el campo lideres muestre los lideres disponibles que asisten al grupo raiz de la iglesia si la red
        ingresada no tiene ningún grupo.
        """

        raiz = Grupo.objects.get(id=1)
        otro = Grupo.objects.get(id=3)
        red_nueva = RedFactory(nombre='nueva red')
        miembro = MiembroFactory(lider=True, grupo=raiz)

        form = NuevoGrupoForm(red=red_nueva)

        self.assertIn(miembro, form.fields['lideres'].queryset)
        self.assertNotIn(otro.lideres.first(), form.fields['lideres'].queryset)
