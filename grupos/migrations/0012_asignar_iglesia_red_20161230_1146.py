# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def asignar_iglesia(apps, schema_editor):
    """
    Asigna una iglesia a las redes. Si no hay iglesia en la bd se crea una.
    """

    Iglesia = apps.get_model('iglesias', 'Iglesia')
    Red = apps.get_model('grupos', 'Red')

    iglesia = Iglesia.objects.first()
    if iglesia is None:
        iglesia = Iglesia.objects.create(nombre='siiom')

    Red.objects.update(iglesia=iglesia)


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0011_red_iglesia'),
        ('iglesias', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(asignar_iglesia, reverse_code=migrations.RunPython.noop)
    ]
