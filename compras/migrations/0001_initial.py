# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compras.models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjunto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('archivo', models.FileField(upload_to=compras.models.Adjunto.ruta_adjuntos, verbose_name='archivo')),
            ],
            options={
                'verbose_name_plural': 'adjuntos',
                'verbose_name': 'adjunto',
            },
        ),
        migrations.CreateModel(
            name='DetalleRequisicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField(blank=True, null=True, verbose_name='cantidad')),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('referencia', models.CharField(blank=True, max_length=50, verbose_name='referencia')),
                ('marca', models.CharField(blank=True, max_length=100, verbose_name='marca')),
                ('valor_aprobado', models.PositiveIntegerField(blank=True, null=True, verbose_name='valor unitario')),
                ('total_aprobado', models.PositiveIntegerField(blank=True, null=True, verbose_name='valor total')),
                ('forma_pago', models.CharField(blank=True, max_length=1, choices=[('E', 'EFECTIVO'), ('D', 'CHEQUE'), ('C', 'CRÉDITO')], verbose_name='forma de pago')),
                ('cumplida', models.BooleanField(verbose_name='cumplida', default=False)),
            ],
            options={
                'verbose_name_plural': 'detalles de la requisición',
                'verbose_name': 'detalle de la requisición',
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('observacion', models.TextField(blank=True, verbose_name='observación')),
                ('estado', models.CharField(max_length=1, choices=[('A', 'Aprobada'), ('R', 'Rechazada')], verbose_name='estado')),
                ('empleado', models.ForeignKey(to='organizacional.Empleado', verbose_name='empleado')),
            ],
            options={
                'verbose_name_plural': 'historial',
                'verbose_name': 'historial',
            },
        ),
        migrations.CreateModel(
            name='Parametros',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dias_habiles', models.PositiveSmallIntegerField(verbose_name='dias hábiles')),
                ('tope_monto', models.PositiveIntegerField(verbose_name='monto tope para presidencia')),
            ],
            options={
                'verbose_name_plural': 'parametros',
                'verbose_name': 'parametro',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('identificacion', models.BigIntegerField(verbose_name='identificación')),
                ('codigo', models.CharField(blank=True, max_length=200, verbose_name='código')),
                ('correo', models.EmailField(max_length=254, verbose_name='email')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='teléfono')),
                ('celular', models.IntegerField(blank=True, null=True, verbose_name='celular')),
                ('contacto', models.CharField(blank=True, max_length=255, verbose_name='contacto')),
            ],
            options={
                'verbose_name_plural': 'proveedores',
                'verbose_name': 'proveedor',
            },
        ),
        migrations.CreateModel(
            name='Requisicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True, verbose_name='fecha de ingreso')),
                ('observaciones', models.TextField(verbose_name='observaciones')),
                ('asunto', models.CharField(max_length=255, verbose_name='asunto')),
                ('prioridad', models.CharField(max_length=1, choices=[('A', 'ALTA'), ('B', 'MEDIA'), ('C', 'BAJA')], verbose_name='prioridad')),
                ('estado', models.CharField(verbose_name='estado', max_length=2, choices=[('PE', 'PENDIENTE'), ('PR', 'PROCESO'), ('TE', 'TERMINADA'), ('AN', 'RECHAZADA')], default='PE')),
                ('fecha_pago', models.DateField(blank=True, null=True, verbose_name='fecha de pago')),
                ('fecha_termina', models.DateField(blank=True, null=True, verbose_name='fecha terminada')),
                ('form_pago', models.CharField(blank=True, max_length=1, choices=[('E', 'EFECTIVO'), ('C', 'CRÉDITO')], verbose_name='forma de pago')),
                ('estado_pago', models.CharField(blank=True, max_length=2, choices=[('PP', 'PAGO AL PROVEEDOR'), ('AP', 'ANTICIPO AL PROVEEDOR'), ('EP', 'EFECTIVO AL PROVEEDOR')], verbose_name='estado de pago')),
                ('presupuesto_aprobado', models.CharField(blank=True, max_length=2, choices=[('SI', 'SI'), ('ES', 'EN ESPERA')], verbose_name='presupuesto aprobado')),
                ('fecha_solicitud', models.DateField(blank=True, null=True, verbose_name='fecha solicitud recurso')),
                ('fecha_proyeccion', models.DateField(blank=True, null=True, verbose_name='fecha proyección pago')),
                ('empleado', models.ForeignKey(to='organizacional.Empleado', verbose_name='empleado')),
            ],
            options={
                'verbose_name_plural': 'requisiciones',
                'verbose_name': 'requisición',
            },
        ),
        migrations.AddField(
            model_name='historial',
            name='requisicion',
            field=models.ForeignKey(to='compras.Requisicion', verbose_name='requisición'),
        ),
        migrations.AddField(
            model_name='detallerequisicion',
            name='proveedor',
            field=models.ForeignKey(verbose_name='proveedor', blank=True, to='compras.Proveedor', null=True),
        ),
        migrations.AddField(
            model_name='detallerequisicion',
            name='requisicion',
            field=models.ForeignKey(to='compras.Requisicion', verbose_name='requisición'),
        ),
        migrations.AddField(
            model_name='adjunto',
            name='requisicion',
            field=models.ForeignKey(to='compras.Requisicion', verbose_name='requisición'),
        ),
    ]
