# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0003_auto_20160713_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjunto',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('archivo', models.FileField(upload_to='', verbose_name='archivo')),
            ],
            options={
                'verbose_name_plural': 'adjuntos',
                'verbose_name': 'adjunto',
            },
        ),
        migrations.CreateModel(
            name='DetalleRequisicion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('cantidad', models.PositiveIntegerField(null=True, verbose_name='cantidad', blank=True)),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('referencia', models.CharField(blank=True, max_length=50, verbose_name='referncia')),
                ('marca', models.CharField(blank=True, max_length=100, verbose_name='marca')),
                ('valor_aprobado', models.PositiveIntegerField(null=True, verbose_name='valor aprobado', blank=True)),
                ('valor_pago', models.PositiveIntegerField(null=True, verbose_name='valor pago', blank=True)),
                ('forma_pago', models.CharField(choices=[('E', 'EFECTIVO'), ('D', 'DEBITO'), ('C', 'CRÉDITO')], blank=True, max_length=1, verbose_name='forma de pago')),
            ],
            options={
                'verbose_name_plural': 'detalles de la requisición',
                'verbose_name': 'detalle de la requisición',
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('fecha', models.DateTimeField(verbose_name='fecha', auto_now_add=True)),
                ('observacion', models.TextField(blank=True, verbose_name='observación')),
                ('estado', models.CharField(choices=[('A', 'Aprobada'), ('R', 'Rechazada')], max_length=1, verbose_name='estado')),
                ('empleado', models.ForeignKey(to='organizacional.Empleado', verbose_name='empleado')),
            ],
            options={
                'verbose_name_plural': 'historial',
                'verbose_name': 'historial',
            },
        ),
        migrations.CreateModel(
            name='Requisicion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('fecha_ingreso', models.DateTimeField(verbose_name='fecha de ingreso', auto_now_add=True)),
                ('observaciones', models.TextField(verbose_name='observaciones')),
                ('prioridad', models.CharField(choices=[('A', 'ALTA'), ('M', 'MEDIA'), ('B', 'BAJA')], max_length=1, verbose_name='prioridad')),
                ('estado', models.CharField(choices=[('PE', 'PENDIENTE'), ('PR', 'PROCESO'), ('TE', 'TERMINADA'), ('AN', 'ANULADA')], max_length=2, default='PE', verbose_name='estado')),
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
            name='requisicion',
            field=models.ForeignKey(to='compras.Requisicion', verbose_name='requisición'),
        ),
        migrations.AddField(
            model_name='adjunto',
            name='requisicion',
            field=models.ForeignKey(to='compras.Requisicion', verbose_name='requisición'),
        ),
    ]
