# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0006_auto_20161025_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupo',
            options={'verbose_name_plural': 'grupos', 'verbose_name': 'grupo'},
        ),
        migrations.AddField(
            model_name='grupo',
            name='parent',
            field=models.ForeignKey(related_name='children_set', verbose_name='padre', to='grupos.Grupo', null=True),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='barrio',
            field=models.ForeignKey(to='miembros.Barrio', verbose_name='barrio'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='diaDiscipulado',
            field=models.CharField(choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], null=True, max_length=1, verbose_name='dia discipulado', blank=True),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='diaGAR',
            field=models.CharField(choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], max_length=1, verbose_name='dia G.A.R'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='direccion',
            field=models.CharField(max_length=50, verbose_name='dirección'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='estado',
            field=models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], max_length=1, verbose_name='estado'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='fechaApertura',
            field=models.DateField(verbose_name='fecha de apertura'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='horaDiscipulado',
            field=models.TimeField(null=True, verbose_name='hora discipulado', blank=True),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='horaGAR',
            field=models.TimeField(verbose_name='hora G.A.R'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='lider1',
            field=models.ForeignKey(related_name='lider_uno', blank=True, to='miembros.Miembro', null=True),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='nombre',
            field=models.CharField(max_length=30, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='red',
            field=models.ForeignKey(blank=True, verbose_name='red', to='grupos.Red', null=True),
        ),
    ]
