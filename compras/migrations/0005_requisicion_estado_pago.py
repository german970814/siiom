# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0004_auto_20160804_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='estado_pago',
            field=models.CharField(max_length=2, verbose_name='estado de pago', choices=[('PP', 'PAGO AL PROVEEDOR'), ('AP', 'ANTICIPO AL PROVEEDOR'), ('EP', 'EFECTIVO AL PROVEEDOR')], blank=True),
        ),
    ]
