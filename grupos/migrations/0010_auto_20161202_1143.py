# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0009_auto_20161121_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupo',
            name='lider1',
        ),
        migrations.RemoveField(
            model_name='grupo',
            name='lider2',
        ),
    ]
