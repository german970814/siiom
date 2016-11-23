# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqr', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caso',
            options={'verbose_name_plural': 'Casos PQR', 'verbose_name': 'Caso PQR'},
        ),
        migrations.AlterModelOptions(
            name='invitacion',
            options={'verbose_name_plural': 'Invitaciones', 'verbose_name': 'Invitación'},
        ),
    ]
