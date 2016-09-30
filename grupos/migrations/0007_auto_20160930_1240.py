# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0006_llenar_grupo_parent_20160927_1747'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupo',
            options={'verbose_name': 'grupo', 'verbose_name_plural': 'grupos'},
        ),
        migrations.AlterField(
            model_name='grupo',
            name='barrio',
            field=models.ForeignKey(verbose_name='barrio', to='miembros.Barrio'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='diaDiscipulado',
            field=models.CharField(blank=True, verbose_name='dia discipulado', null=True, choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], max_length=1),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='diaGAR',
            field=models.CharField(verbose_name='dia G.A.R', max_length=1, choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')]),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='direccion',
            field=models.CharField(verbose_name='dirección', max_length=50),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='estado',
            field=models.CharField(verbose_name='estado', max_length=1, choices=[('A', 'Activo'), ('I', 'Inactivo')]),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='fechaApertura',
            field=models.DateField(verbose_name='fecha de apertura'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='horaDiscipulado',
            field=models.TimeField(verbose_name='hora discipulado', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='horaGAR',
            field=models.TimeField(verbose_name='hora G.A.R'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='nombre',
            field=models.CharField(verbose_name='nombre', max_length=30),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='parent',
            field=models.ForeignKey(related_name='children_set', null=True, verbose_name='padre', to='grupos.Grupo'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='red',
            field=models.ForeignKey(to='grupos.Red', null=True, blank=True, verbose_name='red'),
        ),
    ]
