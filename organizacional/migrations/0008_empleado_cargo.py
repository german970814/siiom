# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0007_auto_20160827_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='cargo',
            field=models.CharField(default='Empleado de Casa de El Rey', verbose_name='cargo', max_length=150),
            preserve_default=False,
        ),
    ]
