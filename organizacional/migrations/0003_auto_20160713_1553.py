# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0002_auto_20160712_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='cedula',
            field=models.BigIntegerField(verbose_name='cédula', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleado',
            name='primer_apellido',
            field=models.CharField(verbose_name='primer apellido', default='apellido', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleado',
            name='primer_nombre',
            field=models.CharField(verbose_name='primer nombre', default='nombre', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empleado',
            name='segundo_apellido',
            field=models.CharField(blank=True, verbose_name='segundo apellido', max_length=100),
        ),
        migrations.AddField(
            model_name='empleado',
            name='segundo_nombre',
            field=models.CharField(blank=True, verbose_name='segundo nombre', max_length=100),
        ),
    ]
