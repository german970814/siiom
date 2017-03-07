# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0023_auto_20170304_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cambioescalafon',
            name='escalafon',
        ),
        migrations.RemoveField(
            model_name='cambioescalafon',
            name='miembro',
        ),
        migrations.RemoveField(
            model_name='cumplimientopasos',
            name='miembro',
        ),
        migrations.RemoveField(
            model_name='cumplimientopasos',
            name='paso',
        ),
        migrations.AlterModelOptions(
            name='miembro',
            options={'permissions': (('es_agente', 'define si un miembro es agente'), ('es_lider', 'indica si el usuario es lider de un GAR'), ('es_administrador', 'es adminisitrador'), ('es_pastor', 'indica si un miembro es pastor'), ('es_tesorero', 'indica si un miembro es tesorero'), ('es_coordinador', 'indica si un miembro es coordinador'), ('buscar_todos', 'indica si un usuario puede buscar miembros'))},
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='escalafon',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='pasos',
        ),
        migrations.DeleteModel(
            name='CambioEscalafon',
        ),
        migrations.DeleteModel(
            name='CumplimientoPasos',
        ),
        migrations.DeleteModel(
            name='Escalafon',
        ),
        migrations.DeleteModel(
            name='Pasos',
        ),
    ]
