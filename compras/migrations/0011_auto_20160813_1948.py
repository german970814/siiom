# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0010_auto_20160811_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallerequisicion',
            name='cumplida',
            field=models.BooleanField(default=False, verbose_name='cumplida'),
        ),
        migrations.AlterField(
            model_name='detallerequisicion',
            name='forma_pago',
            field=models.CharField(choices=[('E', 'EFECTIVO'), ('D', 'CHEQUE'), ('C', 'CRÉDITO')], verbose_name='forma de pago', blank=True, max_length=1),
        ),
    ]
