# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compras.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adjunto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('archivo', models.FileField(verbose_name='archivo', upload_to=compras.models.Adjunto.ruta_adjuntos)),
            ],
            options={
                'verbose_name': 'adjunto',
                'verbose_name_plural': 'adjuntos',
            },
        ),
        migrations.CreateModel(
            name='DetalleRequisicion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(blank=True, null=True, verbose_name='cantidad')),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('referencia', models.CharField(blank=True, max_length=50, verbose_name='referencia')),
                ('marca', models.CharField(blank=True, max_length=100, verbose_name='marca')),
                ('valor_aprobado', models.PositiveIntegerField(blank=True, null=True, verbose_name='valor unitario')),
                ('total_aprobado', models.PositiveIntegerField(blank=True, null=True, verbose_name='valor total')),
                ('forma_pago', models.CharField(choices=[('E', 'EFECTIVO'), ('D', 'CHEQUE'), ('C', 'CRÉDITO')], blank=True, max_length=1, verbose_name='forma de pago')),
                ('cumplida', models.BooleanField(default=False, verbose_name='cumplida')),
            ],
            options={
                'verbose_name': 'detalle de la requisición',
                'verbose_name_plural': 'detalles de la requisición',
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('observacion', models.TextField(blank=True, verbose_name='observación')),
                ('estado', models.CharField(choices=[('A', 'Aprobada'), ('R', 'Rechazada')], verbose_name='estado', max_length=1)),
            ],
            options={
                'verbose_name': 'historial',
                'verbose_name_plural': 'historial',
            },
        ),
        migrations.CreateModel(
            name='Parametros',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('dias_habiles', models.PositiveSmallIntegerField(verbose_name='dias hábiles')),
                ('tope_monto', models.PositiveIntegerField(verbose_name='monto tope para presidencia')),
            ],
            options={
                'verbose_name': 'parametro',
                'verbose_name_plural': 'parametros',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=255)),
                ('identificacion', models.BigIntegerField(verbose_name='identificación')),
                ('codigo', models.CharField(blank=True, max_length=200, verbose_name='código')),
                ('correo', models.EmailField(verbose_name='email', max_length=254)),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='teléfono')),
                ('celular', models.IntegerField(blank=True, null=True, verbose_name='celular')),
                ('contacto', models.CharField(blank=True, max_length=255, verbose_name='contacto')),
            ],
            options={
                'verbose_name': 'proveedor',
                'verbose_name_plural': 'proveedores',
            },
        ),
        migrations.CreateModel(
            name='Requisicion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True, verbose_name='fecha de ingreso')),
                ('observaciones', models.TextField(verbose_name='observaciones')),
                ('asunto', models.CharField(verbose_name='asunto', max_length=255)),
                ('prioridad', models.CharField(choices=[('A', 'ALTA'), ('B', 'MEDIA'), ('C', 'BAJA')], verbose_name='prioridad', max_length=1)),
                ('estado', models.CharField(choices=[('PE', 'PENDIENTE'), ('PR', 'PROCESO'), ('TE', 'TERMINADA'), ('AN', 'RECHAZADA')], verbose_name='estado', default='PE', max_length=2)),
                ('fecha_pago', models.DateField(blank=True, null=True, verbose_name='fecha de pago')),
                ('fecha_termina', models.DateField(blank=True, null=True, verbose_name='fecha terminada')),
                ('form_pago', models.CharField(choices=[('E', 'EFECTIVO'), ('C', 'CRÉDITO')], blank=True, max_length=1, verbose_name='forma de pago')),
                ('estado_pago', models.CharField(choices=[('PP', 'PAGO AL PROVEEDOR'), ('AP', 'ANTICIPO AL PROVEEDOR'), ('EP', 'EFECTIVO AL PROVEEDOR')], blank=True, max_length=2, verbose_name='estado de pago')),
                ('presupuesto_aprobado', models.CharField(choices=[('SI', 'SI'), ('ES', 'EN ESPERA')], blank=True, max_length=2, verbose_name='presupuesto aprobado')),
                ('fecha_solicitud', models.DateField(blank=True, null=True, verbose_name='fecha solicitud recurso')),
                ('fecha_proyeccion', models.DateField(blank=True, null=True, verbose_name='fecha proyección pago')),
            ],
            options={
                'verbose_name': 'requisición',
                'verbose_name_plural': 'requisiciones',
            },
        ),
    ]
