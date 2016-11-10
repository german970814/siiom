# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compras.models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_auto_20160801_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjunto',
            name='archivo',
            field=models.FileField(upload_to=compras.models.Adjunto.ruta_adjuntos, verbose_name='archivo'),
        ),
        migrations.AlterField(
            model_name='detallerequisicion',
            name='forma_pago',
            field=models.CharField(blank=True, max_length=1, choices=[('E', 'EFECTIVO'), ('D', 'DÉBITO'), ('C', 'CRÉDITO')], verbose_name='forma de pago'),
        ),
        migrations.AlterField(
            model_name='detallerequisicion',
            name='referencia',
            field=models.CharField(max_length=50, verbose_name='referencia', blank=True),
        ),
    ]
