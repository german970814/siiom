# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0008_auto_20160811_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisicion',
            name='presupuesto_aprobado',
            field=models.CharField(blank=True, verbose_name='presupuesto aprobado', choices=[('SI', 'SI'), ('ES', 'EN ESPERA')], max_length=2),
        ),
    ]
