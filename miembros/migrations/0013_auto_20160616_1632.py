# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0012_auto_20160601_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cambioescalafon',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
