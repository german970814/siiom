# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuentros', '0003_remove_encuentro_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentro',
            name='estado',
            field=models.CharField(verbose_name='Estado', default='A', max_length=1, choices=[('A', 'ACTIVO'), ('I', 'INACTIVO')]),
        ),
    ]
