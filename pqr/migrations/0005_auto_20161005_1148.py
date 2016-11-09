# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqr', '0004_auto_20161003_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='caso',
            field=models.ForeignKey(to='pqr.Caso', verbose_name='Caso', related_name='documentos'),
        ),
    ]
