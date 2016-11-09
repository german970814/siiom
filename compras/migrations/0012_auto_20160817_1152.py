# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0011_auto_20160813_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisicion',
            name='prioridad',
            field=models.CharField(choices=[('A', 'ALTA'), ('B', 'MEDIA'), ('C', 'BAJA')], max_length=1, verbose_name='prioridad'),
        ),
    ]
