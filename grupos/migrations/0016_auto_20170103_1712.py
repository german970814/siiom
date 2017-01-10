# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0015_asignar_iglesia_20170103_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='iglesia',
            field=models.ForeignKey(to='iglesias.Iglesia', verbose_name='iglesia'),
        ),
    ]
