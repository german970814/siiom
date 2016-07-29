# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuentros', '0004_encuentro_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encontrista',
            name='identificacion',
            field=models.BigIntegerField(verbose_name='Identificación'),
        ),
    ]
