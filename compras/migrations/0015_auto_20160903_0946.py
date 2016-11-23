# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0014_requisicion_fecha_termina'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requisicion',
            name='proveedores',
        ),
        migrations.AddField(
            model_name='detallerequisicion',
            name='proveedor',
            field=models.ForeignKey(null=True, blank=True, verbose_name='proveedor', to='compras.Proveedor'),
        ),
    ]
