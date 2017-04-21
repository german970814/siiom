# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0002_auto_20170405_1756'),
        ('miembros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaSesiones',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('asistencia', models.BooleanField(default=False)),
                ('tarea', models.BooleanField(default=False)),
                ('fecha', models.DateField()),
            ],
            options={
                'get_latest_by': 'fecha',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=1, choices=[('A', 'Abierto'), ('C', 'Cerrado')])),
                ('dia', models.CharField(max_length=1, choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')])),
                ('hora', models.TimeField()),
                ('material', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('fechaInicio', models.DateField()),
                ('notaDefinitiva', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('pago', models.PositiveIntegerField(default=0)),
                ('curso', models.ForeignKey(to='academia.Curso')),
                ('estudiante', models.ForeignKey(to='miembros.Miembro', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=300)),
                ('porcentaje', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nota', models.DecimalField(decimal_places=2, max_digits=3)),
                ('matricula', models.ForeignKey(to='academia.Matricula')),
                ('modulo', models.ForeignKey(to='academia.Modulo')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=500)),
                ('modulo', models.ForeignKey(to='academia.Modulo')),
            ],
        ),
        migrations.AddField(
            model_name='matricula',
            name='moduloActual',
            field=models.ForeignKey(to='academia.Modulo', blank=True, verbose_name='Modulo', related_name='modulo_actual', null=True),
        ),
        migrations.AddField(
            model_name='matricula',
            name='modulos',
            field=models.ManyToManyField(to='academia.Modulo', through='academia.Reporte', related_name='reporte_modulo'),
        ),
        migrations.AddField(
            model_name='matricula',
            name='sesiones',
            field=models.ManyToManyField(to='academia.Sesion', through='academia.AsistenciaSesiones'),
        ),
        migrations.AddField(
            model_name='curso',
            name='modulos',
            field=models.ManyToManyField(to='academia.Modulo'),
        ),
        migrations.AddField(
            model_name='curso',
            name='profesor',
            field=models.ForeignKey(to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='curso',
            name='red',
            field=models.ForeignKey(to='grupos.Red'),
        ),
        migrations.AddField(
            model_name='asistenciasesiones',
            name='matricula',
            field=models.ForeignKey(to='academia.Matricula'),
        ),
        migrations.AddField(
            model_name='asistenciasesiones',
            name='sesion',
            field=models.ForeignKey(to='academia.Sesion'),
        ),
        migrations.AlterUniqueTogether(
            name='reporte',
            unique_together=set([('matricula', 'modulo')]),
        ),
        migrations.AlterUniqueTogether(
            name='asistenciasesiones',
            unique_together=set([('matricula', 'sesion')]),
        ),
    ]
