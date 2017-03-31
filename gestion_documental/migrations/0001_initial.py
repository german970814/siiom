# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gestion_documental.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('archivo', models.FileField(verbose_name='archivo', upload_to=gestion_documental.models.Documento.ruta_archivo)),
            ],
            options={
                'verbose_name': 'documento',
                'verbose_name_plural': 'documentos',
            },
        ),
        migrations.CreateModel(
            name='PalabraClave',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=250, unique=True)),
            ],
            options={
                'verbose_name': 'palabra clave',
                'verbose_name_plural': 'palabras claves',
            },
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('fecha', models.DateField(verbose_name='fecha')),
                ('estante', models.IntegerField(verbose_name='estante')),
                ('caja', models.IntegerField(verbose_name='caja')),
                ('ultima_modificacion', models.DateField(blank=True, null=True, verbose_name='Fecha Última Modificación')),
            ],
            options={
                'verbose_name': 'registro',
                'verbose_name_plural': 'registros',
            },
        ),
        migrations.CreateModel(
            name='SolicitudCustodiaDocumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha_solicitud', models.DateField(auto_now_add=True, verbose_name='Fecha Solicitud')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('estado', models.CharField(choices=[('PE', 'PENDIENTE'), ('RE', 'REALIZADO'), ('PR', 'PROCESO')], verbose_name='Estado', default='PE', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudRegistro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('estado', models.CharField(choices=[('PE', 'PENDIENTE'), ('ED', 'ENTREGADO POR DIGITADOR'), ('DC', 'DEVUELTO POR USUARIO DE CONSULTA')], verbose_name='Estado Solicitud', max_length=2)),
                ('fecha_solicitud', models.DateField(auto_now_add=True, verbose_name='Fecha Solicitud')),
                ('fecha_devolucion', models.DateField(blank=True, null=True, verbose_name='Fecha Devolución')),
                ('comentario', models.TextField(blank=True, verbose_name='Comentario')),
            ],
            options={
                'verbose_name': 'Solicitud de Registro',
                'verbose_name_plural': 'Solicitudes de Registro',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=100)),
            ],
            options={
                'verbose_name': 'tipo de documento',
                'verbose_name_plural': 'tipos de documento',
            },
        ),
    ]
