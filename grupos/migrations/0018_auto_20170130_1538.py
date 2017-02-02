# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import datetime


def migrar_estado_grupos(apps, schema_editor):
    """Funcion para migrar el estado de los grupos."""

    FECHA_HISTORIAL_BASE = datetime.date(year=2014, month=1, day=1)
    Grupo = apps.get_model('grupos', "Grupo")
    Historial = apps.get_model('grupos', "HistorialEstado")

    for grupo in Grupo.objects.all():
        kwargs = {'grupo': grupo, 'fecha': FECHA_HISTORIAL_BASE}
        if grupo.estado == 'I':
            kwargs['estado'] = 'IN'
        else:
            kwargs['estado'] = 'AC'
        Historial.objects.create(**kwargs)


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0017_historial'),
    ]

    operations = [
        migrations.RunPython(migrar_estado_grupos, reverse_code=migrations.RunPython.noop)
    ]
