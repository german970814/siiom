# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0003_remove_red_iglesia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupo',
            name='iglesia',
        ),
    ]
