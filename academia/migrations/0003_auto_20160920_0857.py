# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0002_auto_20160201_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sesion',
            name='nombre',
            field=models.CharField(max_length=500),
        ),
    ]
