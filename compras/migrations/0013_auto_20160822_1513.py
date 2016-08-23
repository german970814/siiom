# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0012_auto_20160817_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=255)),
                ('identificacion', models.BigIntegerField(verbose_name='identificación')),
                ('codigo', models.CharField(verbose_name='código', blank=True, max_length=200)),
                ('correo', models.EmailField(verbose_name='email', max_length=254)),
                ('telefono', models.IntegerField(verbose_name='teléfono', blank=True, null=True)),
                ('celular', models.IntegerField(verbose_name='celular', blank=True, null=True)),
                ('contacto', models.CharField(verbose_name='contacto', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'proveedor',
                'verbose_name_plural': 'proveedores',
            },
        ),
        migrations.AddField(
            model_name='requisicion',
            name='proveedores',
            field=models.ManyToManyField(to='compras.Proveedor', verbose_name='proveedores', blank=True, null=True, related_name='requisiciones'),
        ),
    ]
