# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0012_asignar_iglesia_red_20161230_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='red',
            name='iglesia',
            field=models.ForeignKey(to='iglesias.Iglesia', verbose_name='iglesia'),
        ),
    ]
