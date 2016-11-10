# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0013_auto_20160822_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='fecha_termina',
            field=models.DateField(null=True, blank=True, verbose_name='fecha terminada'),
        ),
    ]
