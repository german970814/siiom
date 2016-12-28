# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def asignar_iglesia(apps, schema_editor):
    """
    Asigna una iglesia a todos los miembros. Si no hay iglesia en la bd se crea una.
    """

    Iglesia = apps.get_model('iglesias', 'Iglesia')
    Miembro = apps.get_model('miembros', 'Miembro')

    iglesia = Iglesia.objects.first()
    if iglesia is None:
        iglesia = Iglesia.objects.create(nombre='siiom')

    Miembro.objects.update(iglesia=iglesia)


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0016_miembro_iglesia'),
        ('iglesias', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(asignar_iglesia, reverse_code=migrations.RunPython.noop)
    ]
