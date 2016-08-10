# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0006_requisicion_asunto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallerequisicion',
            name='total_aprobado',
            field=models.PositiveIntegerField(verbose_name='valor total', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detallerequisicion',
            name='valor_aprobado',
            field=models.PositiveIntegerField(verbose_name='valor unitario', blank=True, null=True),
        ),
    ]
