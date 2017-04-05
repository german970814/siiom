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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('primer_nombre', models.CharField(max_length=60, verbose_name='Primer Nombre')),
                ('segundo_nombre', models.CharField(blank=True, max_length=60, verbose_name='Segundo Nombre')),
                ('primer_apellido', models.CharField(max_length=60, verbose_name='Primer Apellido')),
                ('segundo_apellido', models.CharField(blank=True, max_length=60, verbose_name='Segundo Apellido')),
                ('talla', models.CharField(blank=True, max_length=3, verbose_name='Talla')),
                ('genero', models.CharField(max_length=1, choices=[('M', 'MASCULINO'), ('F', 'FEMENINO')], verbose_name='Género')),
                ('identificacion', models.BigIntegerField(verbose_name='Identificación')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('asistio', models.BooleanField(verbose_name='Asistio', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Encuentro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha_inicial', models.DateTimeField(verbose_name='Fecha Inicial')),
                ('fecha_final', models.DateField(verbose_name='Fecha Final')),
                ('hotel', models.CharField(max_length=100, verbose_name='Hotel')),
                ('direccion', models.CharField(blank=True, max_length=100, verbose_name='Direccion')),
                ('observaciones', models.TextField(blank=True, verbose_name='Observaciones')),
                ('dificultades', models.TextField(blank=True, verbose_name='Dificultades')),
                ('estado', models.CharField(verbose_name='Estado', max_length=1, choices=[('A', 'ACTIVO'), ('I', 'INACTIVO')], default='A')),
            ],
        ),
    ]
