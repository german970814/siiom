# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('primer_nombre', models.CharField(verbose_name='primer nombre', max_length=255)),
                ('segundo_nombre', models.CharField(blank=True, max_length=255, verbose_name='segundo nombre')),
                ('primer_apellido', models.CharField(verbose_name='primer apellido', max_length=255)),
                ('segundo_apellido', models.CharField(blank=True, max_length=255, verbose_name='segundo apellido')),
                ('direccion', models.CharField(blank=True, max_length=255, verbose_name='dirección')),
                ('telefono', models.BigIntegerField(verbose_name='teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('fecha_ingreso', models.DateField(auto_now_add=True, verbose_name='fecha ingreso')),
                ('genero', models.CharField(choices=[('M', 'MASCULINO'), ('F', 'FEMENINO')], verbose_name='género', max_length=1)),
                ('retirado', models.BooleanField(default=False, verbose_name='retirado')),
            ],
        ),
    ]
