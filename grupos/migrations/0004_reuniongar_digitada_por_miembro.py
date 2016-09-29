# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0003_auto_20160824_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='reuniongar',
            name='digitada_por_miembro',
            field=models.BooleanField(default=True),
        ),
    ]
