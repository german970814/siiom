# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0003_auto_20160824_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='parent',
            field=models.ForeignKey(null=True, related_name='children_set', to='grupos.Grupo'),
        ),
    ]
