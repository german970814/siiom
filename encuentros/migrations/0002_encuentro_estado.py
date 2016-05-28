# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuentros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentro',
            name='estado',
            field=models.CharField(default='A', verbose_name='Estado', choices=[('A', 'ACTIVO'), ('I', 'INACTIVO')], max_length=1),
        ),
    ]
