# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0008_llenar_grupo_parent_20161031_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='parent',
            field=models.ForeignKey(verbose_name='grupo origen', related_name='children_set', null=True, to='grupos.Grupo'),
        ),
    ]
