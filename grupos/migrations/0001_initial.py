# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import grupos.six
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('iglesias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaDiscipulado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('asistencia', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('direccion', models.CharField(verbose_name='dirección', max_length=50)),
                ('fechaApertura', models.DateField(verbose_name='fecha de apertura')),
                ('diaGAR', models.CharField(choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], verbose_name='dia G.A.R', max_length=1)),
                ('horaGAR', models.TimeField(verbose_name='hora G.A.R')),
                ('diaDiscipulado', models.CharField(choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], blank=True, max_length=1, null=True, verbose_name='dia discipulado')),
                ('horaDiscipulado', models.TimeField(blank=True, null=True, verbose_name='hora discipulado')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=255)),
                ('latitud', models.FloatField(blank=True, null=True, verbose_name='Latitud')),
                ('longitud', models.FloatField(blank=True, null=True, verbose_name='Longitud')),
            ],
            options={
                'verbose_name': 'grupo',
                'verbose_name_plural': 'grupos',
            },
            bases=(grupos.six.SixALNode, common.models.UtilsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HistorialEstado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='fecha')),
                ('estado', models.CharField(choices=[('AC', 'ACTIVO'), ('IN', 'INACTIVO'), ('SU', 'SUSPENDIDO'), ('AR', 'ARCHIVADO')], verbose_name='estado', max_length=2)),
            ],
            options={
                'verbose_name': 'Historial',
                'ordering': ['-fecha'],
                'verbose_name_plural': 'Historiales',
            },
        ),
        migrations.CreateModel(
            name='Predica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, max_length=500)),
                ('fecha', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Red',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('iglesia', models.ForeignKey(to='iglesias.Iglesia', verbose_name='iglesia')),
            ],
            options={
                'abstract': False,
            },
            bases=(common.models.UtilsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ReunionDiscipulado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('predica', models.CharField(verbose_name='prédica', max_length=100)),
                ('numeroTotalAsistentes', models.PositiveIntegerField(verbose_name='Número total de asistentes')),
                ('numeroLideresAsistentes', models.PositiveIntegerField(verbose_name='Número de líderes asistentes')),
                ('numeroVisitas', models.PositiveIntegerField(verbose_name='Número de visitas:')),
                ('novedades', models.TextField(blank=True, default='nada', null=True, max_length=500)),
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
