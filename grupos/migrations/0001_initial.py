# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import grupos.six


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaDiscipulado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('asistencia', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('direccion', models.CharField(max_length=50, verbose_name='dirección')),
                ('fechaApertura', models.DateField(verbose_name='fecha de apertura')),
                ('diaGAR', models.CharField(max_length=1, choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], verbose_name='dia G.A.R')),
                ('horaGAR', models.TimeField(verbose_name='hora G.A.R')),
                ('diaDiscipulado', models.CharField(blank=True, null=True, max_length=1, choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], verbose_name='dia discipulado')),
                ('horaDiscipulado', models.TimeField(blank=True, null=True, verbose_name='hora discipulado')),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('latitud', models.FloatField(blank=True, null=True, verbose_name='Latitud')),
                ('longitud', models.FloatField(blank=True, null=True, verbose_name='Longitud')),
            ],
            options={
                'verbose_name_plural': 'grupos',
                'verbose_name': 'grupo',
            },
            bases=(grupos.six.SixALNode, models.Model),
        ),
        migrations.CreateModel(
            name='HistorialEstado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('estado', models.CharField(max_length=2, choices=[('AC', 'ACTIVO'), ('IN', 'INACTIVO'), ('SU', 'SUSPENDIDO'), ('AR', 'ARCHIVADO')], verbose_name='estado')),
            ],
            options={
                'ordering': ['-fecha'],
                'verbose_name_plural': 'Historiales',
                'verbose_name': 'Historial',
            },
        ),
        migrations.CreateModel(
            name='Predica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, max_length=500)),
                ('fecha', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Red',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ReunionDiscipulado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('numeroLideresAsistentes', models.PositiveIntegerField(verbose_name='Número de líderes asistentes')),
                ('novedades', models.TextField(max_length=500)),
                ('ofrenda', models.DecimalField(max_digits=19, decimal_places=2)),
                ('confirmacionEntregaOfrenda', models.BooleanField(default=False)),
                ('grupo', models.ForeignKey(to='grupos.Grupo', related_name='reuniones_discipulado')),
                ('predica', models.ForeignKey(to='grupos.Predica', verbose_name='prédica')),
            ],
            options={
                'permissions': (('puede_confirmar_ofrenda_discipulado', 'puede confirmar la entrega de dinero discipulado'),),
            },
        ),
        migrations.CreateModel(
            name='ReunionGAR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateField()),
                ('predica', models.CharField(max_length=100, verbose_name='prédica')),
                ('numeroTotalAsistentes', models.PositiveIntegerField(verbose_name='Número total de asistentes')),
                ('numeroLideresAsistentes', models.PositiveIntegerField(verbose_name='Número de líderes asistentes')),
                ('numeroVisitas', models.PositiveIntegerField(verbose_name='Número de visitas:')),
                ('novedades', models.TextField(blank=True, null=True, max_length=500, default='nada')),
                ('ofrenda', models.DecimalField(max_digits=19, decimal_places=2)),
                ('confirmacionEntregaOfrenda', models.BooleanField(default=False)),
                ('digitada_por_miembro', models.BooleanField(default=True)),
                ('grupo', models.ForeignKey(to='grupos.Grupo', related_name='reuniones_gar')),
            ],
            options={
                'permissions': (('puede_confirmar_ofrenda_GAR', 'puede confirmar la entrega de dinero GAR'),),
            },
        ),
    ]
