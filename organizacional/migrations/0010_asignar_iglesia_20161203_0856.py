# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def asignar_iglesia(apps, schema_editor):
    """
    Asigna una iglesia a todos los empleados. Si la no hay iglesia crea una.
    """

    Iglesia = apps.get_model('iglesias', 'Iglesia')
    Empleado = apps.get_model('organizacional', 'Empleado')

    iglesia = Iglesia.objects.first()
    if iglesia is None:
        iglesia = Iglesia.objects.create(nombre='siiom')

    Empleado.objects.update(iglesia=iglesia)


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0009_empleado_iglesia'),
        ('iglesias', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(asignar_iglesia, migrations.RunPython.noop)
    ]
