# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuentros', '0005_auto_20160715_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encontrista',
            name='grupo',
            field=models.ForeignKey(verbose_name='Grupo', to='grupos.Grupo', related_name='encontristas'),
        ),
    ]
