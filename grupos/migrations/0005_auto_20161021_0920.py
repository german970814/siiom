# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0004_reuniongar_digitada_por_miembro'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='altitud',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Altitud', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grupo',
            name='latitud',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Latitud', blank=True, null=True),
        ),
    ]
