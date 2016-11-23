# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallerequisicion',
            name='valor_pago',
        ),
        migrations.AddField(
            model_name='detallerequisicion',
            name='total_aprobado',
            field=models.PositiveIntegerField(verbose_name='total aprobado', blank=True, null=True),
        ),
    ]
