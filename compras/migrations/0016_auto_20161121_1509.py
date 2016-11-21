# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def crear_parametros_defecto(apps, schema_editor):
    """Crea parametros por defecto"""
    Parametro = apps.get_model('compras', 'Parametros')

    if Parametro.objects.first() is None:
        parametro = Parametro()
        parametro.tope_monto = 2000000
        parametro.dias_habiles = 3
        parametro.save()


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0015_auto_20160903_0946'),
    ]

    operations = [
        migrations.RunPython(crear_parametros_defecto, reverse_code=migrations.RunPython.noop),
    ]
