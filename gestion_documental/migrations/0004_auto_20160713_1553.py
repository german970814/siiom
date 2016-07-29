# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_documental', '0003_auto_20160620_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='caja',
            field=models.IntegerField(verbose_name='caja', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registro',
            name='estante',
            field=models.IntegerField(verbose_name='estante', default=1),
            preserve_default=False,
        ),
    ]
