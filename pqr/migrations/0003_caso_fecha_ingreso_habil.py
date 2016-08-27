# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqr', '0002_auto_20160825_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='caso',
            name='fecha_ingreso_habil',
            field=models.DateField(blank=True, null=True, verbose_name='fecha ingreso hábil'),
        ),
    ]
