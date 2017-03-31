# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='empleado',
            field=models.ForeignKey(to='organizacional.Empleado', verbose_name='empleado'),
        ),
        migrations.AddField(
            model_name='historial',
            name='empleado',
            field=models.ForeignKey(to='organizacional.Empleado', verbose_name='empleado'),
        ),
        migrations.AddField(
            model_name='historial',
            name='requisicion',
            field=models.ForeignKey(to='compras.Requisicion', verbose_name='requisición'),
        ),
        migrations.AddField(
            model_name='detallerequisicion',
            name='proveedor',
            field=models.ForeignKey(to='compras.Proveedor', blank=True, verbose_name='proveedor', null=True),
        ),
        migrations.AddField(
            model_name='detallerequisicion',
            name='requisicion',
            field=models.ForeignKey(to='compras.Requisicion', verbose_name='requisición'),
        ),
        migrations.AddField(
            model_name='adjunto',
            name='requisicion',
            field=models.ForeignKey(to='compras.Requisicion', verbose_name='requisición'),
        ),
    ]
