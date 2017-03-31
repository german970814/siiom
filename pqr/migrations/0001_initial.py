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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha_acontecimiento', models.DateField(blank=True, null=True, verbose_name='fecha acontecimiento')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=255)),
                ('identificacion', models.BigIntegerField(verbose_name='identificación')),
                ('direccion', models.CharField(blank=True, max_length=255, verbose_name='dirección')),
                ('telefono', models.BigIntegerField(verbose_name='teléfono')),
                ('email', models.EmailField(verbose_name='email', max_length=254)),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('asunto', models.CharField(verbose_name='asunto', max_length=255)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='fecha registro')),
                ('cerrado', models.BooleanField(default=False, verbose_name='cerrado')),
                ('llave', models.SlugField(verbose_name='llave')),
                ('valido', models.BooleanField(default=False, verbose_name='valido')),
                ('fecha_ingreso_habil', models.DateField(blank=True, null=True, verbose_name='fecha ingreso hábil')),
                ('empleado_cargo', models.ForeignKey(to='organizacional.Empleado', blank=True, related_name='casos_cargo', verbose_name='empleado a cargo', null=True)),
                ('integrantes', models.ManyToManyField(to='organizacional.Empleado', blank=True, related_name='casos_implicado', verbose_name='integrantes')),
            ],
            options={
                'verbose_name': 'Caso PQR',
                'verbose_name_plural': 'Casos PQR',
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('mensaje', models.TextField(verbose_name='mensaje')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('importante', models.BooleanField(default=False, verbose_name='importante')),
                ('documento', models.BooleanField(default=False, verbose_name='documento')),
                ('caso', models.ForeignKey(to='pqr.Caso', verbose_name='caso')),
                ('empleado', models.ForeignKey(to='organizacional.Empleado', verbose_name='empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('archivo', models.FileField(verbose_name='Archivo', upload_to=pqr.models.Documento.ruta_archivo)),
                ('caso', models.ForeignKey(to='pqr.Caso', verbose_name='Caso', related_name='documentos')),
            ],
        ),
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('mensaje', models.TextField(verbose_name='mensaje')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('caso', models.ForeignKey(to='pqr.Caso', verbose_name='caso')),
                ('emisor', models.ForeignKey(to='organizacional.Empleado', verbose_name='emisor', related_name='invitaciones_realizadas')),
                ('receptor', models.ForeignKey(to='organizacional.Empleado', verbose_name='receptor', related_name='invitaciones_recibidas')),
            ],
            options={
                'verbose_name': 'Invitación',
                'verbose_name_plural': 'Invitaciones',
            },
        ),
    ]
