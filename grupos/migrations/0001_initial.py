# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaDiscipulado',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('asistencia', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='AsistenciaMiembro',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('asistencia', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('direccion', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo')], max_length=1)),
                ('fechaApertura', models.DateField(verbose_name='Fecha de Apertura')),
                ('diaGAR', models.CharField(choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], max_length=1, verbose_name='Dia G.A.R')),
                ('horaGAR', models.TimeField(verbose_name='Hora G.A.R')),
                ('diaDiscipulado', models.CharField(choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], max_length=1, verbose_name='Dia Discipulado')),
                ('horaDiscipulado', models.TimeField(verbose_name='Hora Discipulado')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Predica',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(max_length=500, blank=True)),
                ('fecha', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Red',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ReunionDiscipulado',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('numeroLideresAsistentes', models.PositiveIntegerField(verbose_name='Número de líderes asistentes')),
                ('novedades', models.TextField(max_length=500)),
                ('ofrenda', models.DecimalField(decimal_places=2, max_digits=19)),
                ('confirmacionEntregaOfrenda', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('puede_confirmar_ofrenda_discipulado', 'puede confirmar la entrega de dinero discipulado'),),
            },
        ),
        migrations.CreateModel(
            name='ReunionGAR',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateField()),
                ('predica', models.CharField(max_length=100, verbose_name='prédica')),
                ('numeroTotalAsistentes', models.PositiveIntegerField(verbose_name='Número total de asistentes')),
                ('numeroLideresAsistentes', models.PositiveIntegerField(verbose_name='Número de líderes asistentes')),
                ('numeroVisitas', models.PositiveIntegerField(verbose_name='Número de visitas:')),
                ('novedades', models.TextField(max_length=500, blank=True, null=True, default='nada')),
                ('ofrenda', models.DecimalField(decimal_places=2, max_digits=19)),
                ('confirmacionEntregaOfrenda', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('puede_confirmar_ofrenda_GAR', 'puede confirmar la entrega de dinero GAR'),),
            },
        ),
    ]
