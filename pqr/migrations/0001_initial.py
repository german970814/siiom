# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0003_auto_20160713_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_acontecimiento', models.DateField(null=True, verbose_name='fecha acontecimiento', blank=True)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=255)),
                ('identificacion', models.BigIntegerField(verbose_name='identificación')),
                ('direccion', models.CharField(verbose_name='dirección', blank=True, max_length=255)),
                ('telefono', models.BigIntegerField(null=True, verbose_name='teléfono', blank=True)),
                ('email', models.EmailField(verbose_name='email', max_length=254)),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('asunto', models.CharField(verbose_name='asunto', max_length=255)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='fecha registro')),
                ('cerrado', models.BooleanField(default=False, verbose_name='cerrado')),
                ('llave', models.SlugField(verbose_name='llave')),
                ('valido', models.BooleanField(default=False, verbose_name='valido')),
                ('empleado_cargo', models.ForeignKey(null=True, verbose_name='empleado a cargo', related_name='casos_cargo', blank=True, to='organizacional.Empleado')),
                ('integrantes', models.ManyToManyField(null=True, verbose_name='integrantes', related_name='casos_implicado', blank=True, to='organizacional.Empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje', models.TextField(verbose_name='mensaje')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('importante', models.BooleanField(default=False, verbose_name='importante')),
                ('caso', models.ForeignKey(to='pqr.Caso', verbose_name='caso')),
                ('empleado', models.ForeignKey(to='organizacional.Empleado', verbose_name='empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje', models.TextField(verbose_name='mensaje')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('caso', models.ForeignKey(to='pqr.Caso', verbose_name='caso')),
                ('emisor', models.ForeignKey(verbose_name='emisor', related_name='invitaciones_realizadas', to='organizacional.Empleado')),
                ('receptor', models.ForeignKey(verbose_name='receptor', related_name='invitaciones_recibidas', to='organizacional.Empleado')),
            ],
        ),
    ]
