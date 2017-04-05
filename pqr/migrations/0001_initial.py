# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pqr.models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha_acontecimiento', models.DateField(blank=True, null=True, verbose_name='fecha acontecimiento')),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('identificacion', models.BigIntegerField(verbose_name='identificación')),
                ('direccion', models.CharField(blank=True, max_length=255, verbose_name='dirección')),
                ('telefono', models.BigIntegerField(verbose_name='teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('asunto', models.CharField(max_length=255, verbose_name='asunto')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='fecha registro')),
                ('cerrado', models.BooleanField(verbose_name='cerrado', default=False)),
                ('llave', models.SlugField(verbose_name='llave')),
                ('valido', models.BooleanField(verbose_name='valido', default=False)),
                ('fecha_ingreso_habil', models.DateField(blank=True, null=True, verbose_name='fecha ingreso hábil')),
                ('empleado_cargo', models.ForeignKey(related_name='casos_cargo', verbose_name='empleado a cargo', blank=True, to='organizacional.Empleado', null=True)),
                ('integrantes', models.ManyToManyField(blank=True, to='organizacional.Empleado', related_name='casos_implicado', verbose_name='integrantes')),
            ],
            options={
                'verbose_name_plural': 'Casos PQR',
                'verbose_name': 'Caso PQR',
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('mensaje', models.TextField(verbose_name='mensaje')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('importante', models.BooleanField(verbose_name='importante', default=False)),
                ('documento', models.BooleanField(verbose_name='documento', default=False)),
                ('caso', models.ForeignKey(to='pqr.Caso', verbose_name='caso')),
                ('empleado', models.ForeignKey(to='organizacional.Empleado', verbose_name='empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('archivo', models.FileField(upload_to=pqr.models.Documento.ruta_archivo, verbose_name='Archivo')),
                ('caso', models.ForeignKey(verbose_name='Caso', to='pqr.Caso', related_name='documentos')),
            ],
        ),
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('mensaje', models.TextField(verbose_name='mensaje')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('caso', models.ForeignKey(to='pqr.Caso', verbose_name='caso')),
                ('emisor', models.ForeignKey(verbose_name='emisor', to='organizacional.Empleado', related_name='invitaciones_realizadas')),
                ('receptor', models.ForeignKey(verbose_name='receptor', to='organizacional.Empleado', related_name='invitaciones_recibidas')),
            ],
            options={
                'verbose_name_plural': 'Invitaciones',
                'verbose_name': 'Invitación',
            },
        ),
    ]
