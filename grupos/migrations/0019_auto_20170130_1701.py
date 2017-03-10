# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0018_auto_20170130_1538'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historialestado',
            options={'verbose_name': 'Historial', 'verbose_name_plural': 'Historiales'},
        ),
        migrations.AlterField(
            model_name='historialestado',
            name='fecha',
            field=models.DateTimeField(verbose_name='fecha', auto_now_add=True),
        ),
    ]
