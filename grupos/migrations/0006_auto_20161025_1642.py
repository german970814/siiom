# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from django.conf import settings
from consolidacion.utils import clean_direccion
import requests
import time


def space_to_plus(string):
    """
    Retorna un string con los espacios cambiados a '+'
    """
    return string.replace(' ', '+').replace('#', '%23')


def get_location_grupos_by_direccion(apps, schema_editor):
    """
    Función que busca la Latitud y Longitud de un grupo a partir de una direccion
    con ayuda de la API de Google
    """

    if settings.DATABASES['default']['NAME'] != 'panama_prod':
        # Se obtiene el modelo
        Grupo = apps.get_model('grupos', 'Grupo')

        # se crean las constanstes
        _KEY = 'AIzaSyDV2XozAGL_fsiLEAD6fWL3rr3CFFYskec'
        _URL = 'https://maps.googleapis.com/maps/api/geocode/json?address=%(address)s&sensor=false&key=' + _KEY

        for grupo in Grupo.objects.all():
            direccion = clean_direccion(grupo.direccion).lower()
            try:
                if direccion != '' and direccion is not None:
                    response = requests.get(_URL % {'address': space_to_plus(direccion)})
                    _json = response.json()['results'][0]
                    lat, lng = _json['geometry']['location']['lat'], _json['geometry']['location']['lng']
                    grupo.latitud = lat
                    grupo.longitud = lng
                    grupo.save()
                    time.sleep(1.5)
                    continue
                raise ValueError("Direccion está vacia")
            except Exception as exception:
                print("Datos de fallo...")
                print("Exception: %s" % exception)
                print("ID Grupo: %d" % grupo.id)
                print("Direccion Grupo: %s" % grupo.direccion)
                print("_______________")


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0005_auto_20161022_1050'),
    ]

    operations = [
        migrations.RunPython(get_location_grupos_by_direccion, reverse_code=migrations.RunPython.noop),
    ]
