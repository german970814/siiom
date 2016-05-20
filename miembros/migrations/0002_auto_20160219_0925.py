# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cambioescalafon',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 2, 19, 9, 25, 49, 698645)),
        ),
    ]
