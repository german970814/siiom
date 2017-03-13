# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_iglesia_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='iglesia',
            name='termino_gar',
            field=models.CharField(verbose_name='termino GAR', default='GAR', max_length=100),
        ),
        migrations.AddField(
            model_name='iglesia',
            name='termino_visitas',
            field=models.CharField(verbose_name='termino visitas', default='visitas', max_length=100),
        ),
    ]
