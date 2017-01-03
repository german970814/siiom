# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0019_auto_20161130_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembro',
            name='iglesia',
            field=models.ForeignKey(to='iglesias.Iglesia', verbose_name='iglesia'),
        ),
    ]
