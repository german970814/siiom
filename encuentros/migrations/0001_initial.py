# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Encontrista',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('primer_nombre', models.CharField(verbose_name='Primer Nombre', max_length=60)),
                ('segundo_nombre', models.CharField(blank=True, max_length=60, verbose_name='Segundo Nombre')),
                ('primer_apellido', models.CharField(verbose_name='Primer Apellido', max_length=60)),
                ('segundo_apellido', models.CharField(blank=True, max_length=60, verbose_name='Segundo Apellido')),
                ('talla', models.CharField(blank=True, max_length=3, verbose_name='Talla')),
                ('genero', models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMENINO')], verbose_name='Género', max_length=1)),
                ('identificacion', models.BigIntegerField(verbose_name='Identificación')),
                ('email', models.EmailField(verbose_name='Email', max_length=254)),
                ('asistio', models.BooleanField(default=False, verbose_name='Asistio')),
            ],
        ),
        migrations.CreateModel(
            name='Encuentro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha_inicial', models.DateTimeField(verbose_name='Fecha Inicial')),
                ('fecha_final', models.DateField(verbose_name='Fecha Final')),
                ('hotel', models.CharField(verbose_name='Hotel', max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=100, verbose_name='Direccion')),
                ('observaciones', models.TextField(blank=True, verbose_name='Observaciones')),
                ('dificultades', models.TextField(blank=True, verbose_name='Dificultades')),
                ('estado', models.CharField(choices=[('A', 'ACTIVO'), ('I', 'INACTIVO')], verbose_name='Estado', default='A', max_length=1)),
            ],
        ),
    ]
