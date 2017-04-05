# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'áreas',
                'verbose_name': 'área',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='nombre')),
            ],
            options={
                'verbose_name_plural': 'departamentos',
                'verbose_name': 'departamento',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('cedula', models.BigIntegerField(unique=True, verbose_name='cédula')),
                ('primer_nombre', models.CharField(max_length=100, verbose_name='primer nombre')),
                ('segundo_nombre', models.CharField(blank=True, max_length=100, verbose_name='segundo nombre')),
                ('primer_apellido', models.CharField(max_length=100, verbose_name='primer apellido')),
                ('segundo_apellido', models.CharField(blank=True, max_length=100, verbose_name='segundo apellido')),
                ('jefe_departamento', models.BooleanField(verbose_name='jefe de departamento', default=False)),
                ('cargo', models.CharField(max_length=150, verbose_name='cargo')),
                ('areas', models.ManyToManyField(to='organizacional.Area', related_name='empleados', verbose_name='áreas')),
                ('usuario', models.OneToOneField(verbose_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'empleado',
                'permissions': (('es_administrador_sgd', 'Es Administrador de Sistema Gestion Documental'), ('buscar_registros', 'Puede Buscar Registros'), ('es_compras', 'Es usuario de compras'), ('es_presidente', 'Es presidente')),
                'verbose_name_plural': 'empleados',
            },
        ),
        migrations.AddField(
            model_name='area',
            name='departamento',
            field=models.ForeignKey(verbose_name='departamento', to='organizacional.Departamento', related_name='areas'),
        ),
    ]
