# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consolidacion', '0002_auto_20161028_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visita',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email'),
        ),
    ]
