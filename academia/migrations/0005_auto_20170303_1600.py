# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0004_auto_20170303_1558'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='asistenciasesiones',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='asistenciasesiones',
            name='matricula',
        ),
        migrations.RemoveField(
            model_name='asistenciasesiones',
            name='sesion',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='modulos',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='profesor',
        ),
        migrations.RemoveField(
            model_name='curso',
            name='red',
        ),
        migrations.RemoveField(
            model_name='matricula',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='matricula',
            name='estudiante',
        ),
        migrations.RemoveField(
            model_name='matricula',
            name='moduloActual',
        ),
        migrations.RemoveField(
            model_name='matricula',
            name='modulos',
        ),
        migrations.RemoveField(
            model_name='matricula',
            name='sesiones',
        ),
        migrations.AlterUniqueTogether(
            name='reporte',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='matricula',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='modulo',
        ),
        migrations.RemoveField(
            model_name='sesion',
            name='modulo',
        ),
        migrations.DeleteModel(
            name='AsistenciaSesiones',
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
        migrations.DeleteModel(
            name='Matricula',
        ),
        migrations.DeleteModel(
            name='ModuloTania',
        ),
        migrations.DeleteModel(
            name='Reporte',
        ),
        migrations.DeleteModel(
            name='Sesion',
        ),
    ]
