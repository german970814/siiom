# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0002_auto_20170322_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='red',
            name='iglesia',
        ),
    ]
