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
            name='latitud',
            field=models.FloatField(verbose_name='Latitud', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grupo',
            name='longitud',
            field=models.FloatField(verbose_name='Longitud', blank=True, null=True),
        ),
    ]
