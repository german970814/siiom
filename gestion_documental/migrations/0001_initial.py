# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gestion_documental.models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('archivo', models.FileField(upload_to=gestion_documental.models.Documento.ruta_archivo, verbose_name='archivo')),
            ],
            options={
                'verbose_name_plural': 'documentos',
                'verbose_name': 'documento',
            },
        ),
        migrations.CreateModel(
            name='PalabraClave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=250, unique=True, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'palabras claves',
                'verbose_name': 'palabra clave',
            },
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('fecha', models.DateField(verbose_name='fecha')),
                ('estante', models.IntegerField(verbose_name='estante')),
                ('caja', models.IntegerField(verbose_name='caja')),
                ('ultima_modificacion', models.DateField(blank=True, null=True, verbose_name='Fecha Última Modificación')),
                ('area', models.ForeignKey(verbose_name='área', to='organizacional.Area', related_name='registros')),
                ('modificado_por', models.ForeignKey(verbose_name='Modificado Por', blank=True, to='organizacional.Empleado', null=True)),
                ('palabras_claves', models.ManyToManyField(blank=True, to='gestion_documental.PalabraClave', related_name='registros', verbose_name='palabras claves')),
            ],
            options={
                'verbose_name_plural': 'registros',
                'verbose_name': 'registro',
            },
        ),
        migrations.CreateModel(
            name='SolicitudCustodiaDocumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha_solicitud', models.DateField(auto_now_add=True, verbose_name='Fecha Solicitud')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('estado', models.CharField(verbose_name='Estado', max_length=2, choices=[('PE', 'PENDIENTE'), ('RE', 'REALIZADO'), ('PR', 'PROCESO')], default='PE')),
                ('area', models.ForeignKey(to='organizacional.Area', verbose_name='Área')),
                ('solicitante', models.ForeignKey(verbose_name='Solicitante', to='organizacional.Empleado', related_name='solicitudes_custodia')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudRegistro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('estado', models.CharField(max_length=2, choices=[('PE', 'PENDIENTE'), ('ED', 'ENTREGADO POR DIGITADOR'), ('DC', 'DEVUELTO POR USUARIO DE CONSULTA')], verbose_name='Estado Solicitud')),
                ('fecha_solicitud', models.DateField(auto_now_add=True, verbose_name='Fecha Solicitud')),
                ('fecha_devolucion', models.DateField(blank=True, null=True, verbose_name='Fecha Devolución')),
                ('comentario', models.TextField(blank=True, verbose_name='Comentario')),
                ('registro', models.ForeignKey(to='gestion_documental.Registro', verbose_name='Registro')),
                ('usuario_autoriza', models.ForeignKey(related_name='autorizaciones', verbose_name='Autoriza', blank=True, to='organizacional.Empleado', null=True)),
                ('usuario_solicita', models.ForeignKey(verbose_name='Solicitante', to='organizacional.Empleado', related_name='solicitudes')),
            ],
            options={
                'verbose_name_plural': 'Solicitudes de Registro',
                'verbose_name': 'Solicitud de Registro',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
                ('areas', models.ManyToManyField(to='organizacional.Area', related_name='tipos_documento', verbose_name='áreas')),
            ],
            options={
                'verbose_name_plural': 'tipos de documento',
                'verbose_name': 'tipo de documento',
            },
        ),
        migrations.AddField(
            model_name='solicitudcustodiadocumento',
            name='tipo_documento',
            field=models.ForeignKey(to='gestion_documental.TipoDocumento', verbose_name='Tipo de Documento'),
        ),
        migrations.AddField(
            model_name='solicitudcustodiadocumento',
            name='usuario_recibe',
            field=models.ForeignKey(verbose_name='Usuario Recibe Documento', to='organizacional.Empleado', related_name='solicitudes_custodia_recibidas'),
        ),
        migrations.AddField(
            model_name='documento',
            name='registro',
            field=models.ForeignKey(verbose_name='registro', to='gestion_documental.Registro', related_name='documentos'),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo_documento',
            field=models.ForeignKey(verbose_name='tipo de documento', to='gestion_documental.TipoDocumento', related_name='documentos'),
        ),
    ]
