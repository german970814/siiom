# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consolidacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visita',
            name='genero',
            field=models.CharField(default='M', verbose_name='género', max_length=1, choices=[('M', 'MASCULINO'), ('F', 'FEMENINO')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='visita',
            name='retirado',
            field=models.BooleanField(default=False, verbose_name='retirado'),
        ),
    ]
