# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0002_auto_20160201_0932'),
        ('miembros', '0010_auto_20160525_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encontrista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('primer_nombre', models.CharField(verbose_name='Primer Nombre', max_length=60)),
                ('segundo_nombre', models.CharField(verbose_name='Segundo Nombre', max_length=60, blank=True)),
                ('primer_apellido', models.CharField(verbose_name='Primer Apellido', max_length=60)),
                ('segundo_apellido', models.CharField(verbose_name='Segundo Apellido', max_length=60, blank=True)),
                ('talla', models.CharField(verbose_name='Talla', max_length=3, blank=True)),
                ('genero', models.CharField(verbose_name='Género', max_length=1, choices=[('M', 'MASCULINO'), ('F', 'FEMENINO')])),
                ('identificacion', models.IntegerField(verbose_name='Identificación')),
                ('email', models.EmailField(verbose_name='Email', max_length=254)),
                ('asistio', models.BooleanField(verbose_name='Asistio', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Encuentro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha_inicial', models.DateTimeField(verbose_name='Fecha Inicial')),
                ('fecha_final', models.DateField(verbose_name='Fecha Final')),
                ('hotel', models.CharField(verbose_name='Hotel', max_length=100)),
                ('direccion', models.CharField(verbose_name='Direccion', max_length=100, blank=True)),
                ('observaciones', models.TextField(verbose_name='Observaciones', blank=True)),
                ('dificultades', models.TextField(verbose_name='Dificultades', blank=True)),
                ('coordinador', models.ForeignKey(related_name='encuentros_coordinador', verbose_name='Coordinador', to='miembros.Miembro')),
                ('grupos', models.ManyToManyField(verbose_name='Grupos', to='grupos.Grupo')),
                ('tesorero', models.ForeignKey(related_name='encuentros_tesorero', verbose_name='Tesorero', to='miembros.Miembro')),
            ],
        ),
        migrations.AddField(
            model_name='encontrista',
            name='encuentro',
            field=models.ForeignKey(to='encuentros.Encuentro', verbose_name='Encuentro'),
        ),
        migrations.AddField(
            model_name='encontrista',
            name='grupo',
            field=models.ForeignKey(to='grupos.Grupo', verbose_name='Grupo'),
        ),
    ]
