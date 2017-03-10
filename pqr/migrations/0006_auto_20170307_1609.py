# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqr', '0005_auto_20161005_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caso',
            name='integrantes',
            field=models.ManyToManyField(related_name='casos_implicado', blank=True, to='organizacional.Empleado', verbose_name='integrantes'),
        ),
    ]
