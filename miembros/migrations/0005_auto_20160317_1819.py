# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0004_auto_20160219_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cambioescalafon',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 3, 17, 18, 19, 44, 858272)),
        ),
    ]
