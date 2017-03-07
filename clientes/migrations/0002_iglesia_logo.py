# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iglesia',
            name='logo',
            field=models.ImageField(null=True, verbose_name='logo', blank=True, upload_to=''),
        ),
    ]
