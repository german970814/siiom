# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0017_auto_20170119_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reuniondiscipulado',
            name='grupo',
            field=models.ForeignKey(related_name='reuniones_discipulado', to='grupos.Grupo'),
        ),
    ]
