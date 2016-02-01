# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaSesiones',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('A', 'Abierto'), ('C', 'Cerrado')], max_length=1)),
                ('dia', models.CharField(choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], max_length=1)),
                ('hora', models.TimeField()),
                ('material', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fechaInicio', models.DateField()),
                ('notaDefinitiva', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('pago', models.PositiveIntegerField(default=0)),
                ('curso', models.ForeignKey(to='academia.Curso')),
            ],
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=20)),
                ('porcentaje', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=20)),
                ('modulo', models.ForeignKey(to='academia.Modulo')),
            ],
        ),
    ]
