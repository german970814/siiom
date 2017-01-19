# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iglesias', '0001_initial'),
        ('grupos', '0013_auto_20161230_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='iglesia',
            field=models.ForeignKey(null=True, to='iglesias.Iglesia'),
        ),
    ]
