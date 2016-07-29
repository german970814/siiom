# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0003_auto_20160713_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='jefe_departamento',
            field=models.BooleanField(verbose_name='jefe de departamento', default=False),
        ),
    ]
