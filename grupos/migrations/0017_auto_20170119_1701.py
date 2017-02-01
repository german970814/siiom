# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0016_auto_20170103_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reuniongar',
            name='grupo',
            field=models.ForeignKey(to='grupos.Grupo', related_name='reuniones_gar'),
        ),
    ]
