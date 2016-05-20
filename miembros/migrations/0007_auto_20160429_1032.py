# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0006_auto_20160418_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cambioescalafon',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 4, 29, 10, 32, 45, 956091)),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='cedula',
            field=models.CharField(max_length=25, validators=[django.core.validators.RegexValidator('\\d+', 'Se aceptan solo numeros')], verbose_name='cédula', unique=True),
        ),
    ]
