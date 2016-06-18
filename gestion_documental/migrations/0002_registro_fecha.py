# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_documental', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 6, 17, 18, 5, 10, 68373), verbose_name='fecha'),
            preserve_default=False,
        ),
    ]
