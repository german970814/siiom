# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import common.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iglesias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=100)),
            ],
            options={
                'verbose_name': 'área',
                'verbose_name_plural': 'áreas',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=100)),
            ],
            options={
                'verbose_name': 'departamento',
                'verbose_name_plural': 'departamentos',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('cedula', models.BigIntegerField(verbose_name='cédula', unique=True)),
                ('primer_nombre', models.CharField(verbose_name='primer nombre', max_length=100)),
                ('segundo_nombre', models.CharField(blank=True, max_length=100, verbose_name='segundo nombre')),
                ('primer_apellido', models.CharField(verbose_name='primer apellido', max_length=100)),
                ('segundo_apellido', models.CharField(blank=True, max_length=100, verbose_name='segundo apellido')),
                ('jefe_departamento', models.BooleanField(default=False, verbose_name='jefe de departamento')),
                ('cargo', models.CharField(verbose_name='cargo', max_length=150)),
                ('areas', models.ManyToManyField(to='organizacional.Area', verbose_name='áreas', related_name='empleados')),
                ('iglesia', models.ForeignKey(to='iglesias.Iglesia', verbose_name='iglesia')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'empleado',
                'permissions': (('es_administrador_sgd', 'Es Administrador de Sistema Gestion Documental'), ('buscar_registros', 'Puede Buscar Registros'), ('es_compras', 'Es usuario de compras'), ('es_presidente', 'Es presidente')),
                'verbose_name_plural': 'empleados',
            },
            bases=(common.models.UtilsModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='area',
            name='departamento',
            field=models.ForeignKey(to='organizacional.Departamento', verbose_name='departamento', related_name='areas'),
        ),
    ]
