# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import common.models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0002_auto_20170921_1132'),
        ('grupos', '0002_auto_20170405_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abono',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('valor', models.IntegerField(verbose_name='Valor')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('hora_fin', models.TimeField(verbose_name='Hora Fin')),
                ('fecha_fin', models.DateField(verbose_name='Fecha Fin')),
                ('hora_inicio', models.TimeField(verbose_name='Hora Inicio')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha Inicio')),
                ('estado', models.CharField(verbose_name='Estado', max_length=1, choices=[('A', 'Abierto'), ('C', 'Cerrado')])),
                ('dia', models.CharField(verbose_name='Día', max_length=1, choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')])),
            ],
            bases=(common.models.DiasSemanaMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombres', models.CharField(verbose_name='Nombres', max_length=255)),
                ('apellidos', models.CharField(verbose_name='Apellidos', max_length=255)),
                ('identificacion', models.CharField(verbose_name='Identificación', max_length=100)),
                ('grupo', models.ForeignKey(verbose_name='Grupo', related_name='estudiantes', to='grupos.Grupo')),
                ('miembro', models.OneToOneField(verbose_name='Líder', blank=True, null=True, related_name='estudiante', to='miembros.Miembro')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=255)),
                ('grupos_minimo', models.IntegerField(verbose_name='Grupos mínimo', default=0)),
                ('dependencia', models.ForeignKey(blank=True, null=True, related_name='dependecias_set', to='instituto.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('paso', models.NullBooleanField(verbose_name='Pasó')),
                ('curso', models.ForeignKey(verbose_name='Curso', related_name='matriculas', to='instituto.Curso')),
                ('estudiante', models.ForeignKey(verbose_name='Estudiante', related_name='matriculas', to='instituto.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('prioridad', models.IntegerField(verbose_name='Prioridad')),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=255)),
                ('materia', models.ForeignKey(verbose_name='Materia', related_name='modulos', to='instituto.Materia')),
            ],
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=100)),
                ('capacidad', models.IntegerField(verbose_name='Capacidad')),
            ],
        ),
        migrations.CreateModel(
            name='Seguimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('asistencia', models.BooleanField(verbose_name='Asistencia')),
                ('nota', models.IntegerField(verbose_name='Nota')),
                ('matricula', models.ForeignKey(verbose_name='Matricula', related_name='asistencias', to='instituto.Matricula')),
            ],
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('prioridad', models.IntegerField(verbose_name='Prioridad')),
                ('nombre', models.CharField(verbose_name='Nombre', max_length=255)),
                ('modulo', models.ForeignKey(verbose_name='Módulo', related_name='sesiones', to='instituto.Modulo')),
            ],
        ),
        migrations.AddField(
            model_name='seguimiento',
            name='sesion',
            field=models.ForeignKey(verbose_name='Sesión', to='instituto.Sesion'),
        ),
        migrations.AddField(
            model_name='curso',
            name='materia',
            field=models.ForeignKey(verbose_name='Materia', related_name='cursos', to='instituto.Materia'),
        ),
        migrations.AddField(
            model_name='curso',
            name='profesor',
            field=models.ManyToManyField(verbose_name='Profesor', related_name='cursos_como_profesor', to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='curso',
            name='salon',
            field=models.ForeignKey(verbose_name='Salón', related_name='cursos', to='instituto.Salon'),
        ),
        migrations.AddField(
            model_name='abono',
            name='matricula',
            field=models.ForeignKey(related_name='abonos', to='instituto.Materia'),
        ),
    ]
