# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0009_auto_20160811_0906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parametros',
            options={'verbose_name': 'parametro', 'verbose_name_plural': 'parametros'},
        ),
    ]
