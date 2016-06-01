# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def convertir_pecadores(apps, schema_editor):
    Miembro = apps.get_model('miembros', 'Miembro')

    for miembro in Miembro.objects.all():
        if miembro.grupo:
            miembro.convertido = True
            miembro.save()


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0011_auto_20160527_1311'),
    ]

    operations = [
        migrations.RunPython(convertir_pecadores),
    ]
