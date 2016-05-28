# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0010_auto_20160525_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='miembro',
            options={'permissions': (('es_agente', 'define si un miembro es agente'), ('es_lider', 'indica si el usuario es lider de un GAR'), ('es_maestro', 'indica si un usuario es maestro de un curso'), ('es_administrador', 'es adminisitrador'), ('buscar_todos', 'indica si un usuario puede buscar miembros'), ('puede_editar_miembro', 'indica si un usuario puede editar miembros'), ('puede_agregar_visitante', 'puede agregar miembros visitantes'), ('llamada_lider', 'puede modificar llamada lider'), ('llamada_agente', 'puede modificar llamada agente'), ('cumplimiento_pasos', 'puede registrar el cumplimiento de pasos'), ('es_pastor', 'indica si un miembro es pastor'), ('es_tesorero', 'indica si un miembro es tesorero'), ('es_coordinador', 'indica si un miembro es coordinador'))},
        ),
        migrations.AlterField(
            model_name='cambioescalafon',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 5, 27, 13, 11, 25, 596995)),
        ),
    ]
