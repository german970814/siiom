# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iglesias', '0001_initial'),
        ('grupos', '0010_auto_20161202_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='red',
            name='iglesia',
            field=models.ForeignKey(to='iglesias.Iglesia', null=True),
        ),
    ]
