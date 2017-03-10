# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import datetime


def migrar_estado_grupos(apps, schema_editor):
    """Funcion para migrar el estado de los grupos."""

    FECHA_HISTORIAL_BASE = datetime.date(year=2014, month=1, day=1)
    Grupo = apps.get_model('grupos', "Grupo")
    ReunionGAR = apps.get_model('grupos', "ReunionGAR")
    Historial = apps.get_model('grupos', "HistorialEstado")

    for grupo in Grupo.objects.all():
        kwargs = {'grupo': grupo, 'fecha': grupo.fechaApertura}
        if grupo.estado == 'I':
            kwargs['estado'] = 'AC'
            Historial.objects.create(**kwargs)
            kwargs['estado'] = 'IN'
            ultimo_reporte = ReunionGAR.objects.filter(grupo=grupo.id).last()
            if ultimo_reporte is not None:
                kwargs['fecha'] = ultimo_reporte.fecha + datetime.timedelta(weeks=1)
            else:
                kwargs['fecha'] = kwargs['fecha'] + datetime.timedelta(weeks=1)
        else:
            kwargs['estado'] = 'AC'
            kwargs['fecha'] = grupo.fechaApertura
        Historial.objects.create(**kwargs)


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0017_historial'),
    ]

    operations = [
        migrations.RunPython(migrar_estado_grupos, reverse_code=migrations.RunPython.noop)
    ]
