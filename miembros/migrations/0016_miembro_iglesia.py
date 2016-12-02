# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iglesias', '0001_initial'),
        ('miembros', '0015_llenar_grupo_lidera_20161031_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='iglesia',
            field=models.ForeignKey(verbose_name='iglesia', to='iglesias.Iglesia', null=True),
        ),
    ]
