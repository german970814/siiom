# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0005_auto_20161021_0920'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('primer_nombre', models.CharField(max_length=255, verbose_name='primer nombre')),
                ('segundo_nombre', models.CharField(max_length=255, blank=True, verbose_name='segundo nombre')),
                ('primer_apellido', models.CharField(max_length=255, verbose_name='primer apellido')),
                ('segundo_apellido', models.CharField(max_length=255, blank=True, verbose_name='segundo apellido')),
                ('direccion', models.CharField(max_length=255, blank=True, verbose_name='dirección')),
                ('telefono', models.BigIntegerField(verbose_name='teléfono')),
                ('email', models.EmailField(max_length=254, unique=True, blank=True, verbose_name='email')),
                ('fecha_ingreso', models.DateField(auto_now_add=True, verbose_name='fecha ingreso')),
                ('grupo', models.ForeignKey(blank=True, verbose_name='grupo', to='grupos.Grupo', null=True)),
            ],
        ),
    ]
