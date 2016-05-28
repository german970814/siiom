# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuentros', '0002_encuentro_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encuentro',
            name='estado',
        ),
    ]
