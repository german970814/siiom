# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0002_auto_20160201_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='parent',
            field=models.ForeignKey(null=True, to='grupos.Grupo', related_name='children_set'),
        ),
    ]
