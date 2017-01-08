# Django imports
from django.core.urlresolvers import reverse

from .base import BaseTestAPI
from miembros.tests.factories import MiembroFactory, BarrioFactory
from grupos.tests.factories import RedFactory
from grupos.models import Grupo, Red
from .. import constants


class TestAPIBusquedaMiembro(BaseTestAPI):
    """
    Pruebas unitarias para la vista de API que permite hacer las busquedas a los miembros lideres
    que no lideran un grupo.
    """

    def setUp(self):
        self.crear_arbol()
        grupo3 = Grupo.objects.get(id=300)
        self.padre = Grupo.objects.get(id=800)
        self.lider1 = MiembroFactory(lider=True, grupo=grupo3)
        self.lider2 = MiembroFactory(lider=True, grupo=self.padre)
        self.barrio = BarrioFactory()
        self.red_jovenes = Red.objects.get(nombre='jovenes')
        self.url = reverse('common:busqueda_miembro_api', args=(self.red_jovenes.id, ))
        # self.url = '/common/api/buscar_miembro/{}/'.format(self.red_jovenes.id)

    def test_get_not_response(self):
        """Prueba que en GET no se obtienga la respuesta."""

        response = self.GET(login=False)

        self.assertNotIn('miembros', response)
        self.assertIn(constants.RESPONSE_CODE, response)
        self.assertEqual(response[constants.RESPONSE_CODE], constants.RESPONSE_DENIED)

    def test_miembros_in_response(self):
        """
        Prueba que los miembros esten en la respuesta de JSON.
        """

        response = self.POST(data={'value': self.lider1.nombre[0:5]})

        self.assertIn('miembros', response)
        self.assertIn(constants.RESPONSE_CODE, response)
        self.assertEqual(response[constants.RESPONSE_CODE], constants.RESPONSE_SUCCESS)

    def test_busqueda_solo_muestra_lideres(self):
        """
        Prueba que en la busqueda solo se muestren miembros que sean lideres.
        """

        no_lider = MiembroFactory()

        response = self.POST(data={'value': no_lider.nombre[0:5]})

        self.assertEqual(response['miembros'].__len__(), 0)

        lider = MiembroFactory(lider=True, grupo=Grupo.objects.red(self.red_jovenes)[0])

        response = self.POST(data={'value': lider.nombre[0:5]})

        self.assertIn('id', response['miembros'][0])
        self.assertEqual(str(response['miembros'][0]['id']), str(lider.id))

    def test_campo_lideres_solo_muestra_lideres_red_ingresada(self):
        """
        Prueba que el campo lideres solo muestra lideres que pertenecen a los grupos de la red ingresada.
        """

        grupo1 = Grupo.objects.get(id=200)
        lider_joven = MiembroFactory(lider=True, grupo=grupo1)

        response = self.POST(data={'value': lider_joven.nombre[0:5]})

        self.assertEqual(response['miembros'].__len__(), 0)

    def test_campo_lideres_muestra_lideres_raiz_si_red_no_tiene_grupo(self):
        """
        Prueba que el campo lideres muestre los lideres disponibles que asisten al grupo raiz de la iglesia si la red
        ingresada no tiene ningún grupo.
        """

        raiz = Grupo.objects.get(id=100)
        otro = Grupo.objects.get(id=300)

        red_nueva = RedFactory(nombre='nueva red')

        miembro = MiembroFactory(lider=True, grupo=raiz)

        url = reverse('common:busqueda_miembro_api', args=(red_nueva.id, ))

        response = self.POST(url=url, data={'value': miembro.nombre[0:5]})

        self.assertEqual(str(response['miembros'][0]['id']), miembro.id.__str__())

        for m in response['miembros']:
            self.assertNotEqual(str(otro.lideres.first().id), str(m['id']))
