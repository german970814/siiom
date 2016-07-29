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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'áreas',
                'verbose_name': 'área',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'departamentos',
                'verbose_name': 'departamento',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('areas', models.ManyToManyField(to='organizacional.Area', verbose_name='áreas', related_name='empleados')),
                ('usuario', models.OneToOneField(verbose_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'empleados',
                'verbose_name': 'empleado',
            },
        ),
        migrations.AddField(
            model_name='area',
            name='departamento',
            field=models.ForeignKey(verbose_name='departamento', related_name='areas', to='organizacional.Departamento'),
        ),
    ]
