# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consolidacion', '0003_auto_20161029_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visita',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, verbose_name='grupo', to='grupos.Grupo', related_name='visitas'),
        ),
    ]
