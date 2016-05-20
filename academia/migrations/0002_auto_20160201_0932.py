# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0001_initial'),
        ('academia', '0001_initial'),
        ('grupos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matricula',
            name='estudiante',
            field=models.ForeignKey(to='miembros.Miembro', unique=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='moduloActual',
            field=models.ForeignKey(to='academia.Modulo', related_name='modulo_actual', blank=True, null=True, verbose_name='Modulo'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='modulos',
            field=models.ManyToManyField(to='academia.Modulo', related_name='reporte_modulo', through='academia.Reporte'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='sesiones',
            field=models.ManyToManyField(to='academia.Sesion', through='academia.AsistenciaSesiones'),
        ),
        migrations.AddField(
            model_name='curso',
            name='modulos',
            field=models.ManyToManyField(to='academia.Modulo'),
        ),
        migrations.AddField(
            model_name='curso',
            name='profesor',
            field=models.ForeignKey(to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='curso',
            name='red',
            field=models.ForeignKey(to='grupos.Red'),
        ),
        migrations.AddField(
            model_name='asistenciasesiones',
            name='matricula',
            field=models.ForeignKey(to='academia.Matricula'),
        ),
        migrations.AddField(
            model_name='asistenciasesiones',
            name='sesion',
            field=models.ForeignKey(to='academia.Sesion'),
        ),
        migrations.AlterUniqueTogether(
            name='reporte',
            unique_together=set([('matricula', 'modulo')]),
        ),
        migrations.AlterUniqueTogether(
            name='asistenciasesiones',
            unique_together=set([('matricula', 'sesion')]),
        ),
    ]
