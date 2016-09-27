# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0006_llenar_grupo_parent_20160927_1747'),
        ('miembros', '0013_auto_20160616_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='grupo_lidera',
            field=models.ForeignKey(related_name='lideres', null=True, verbose_name='grupo que lidera', blank=True, to='grupos.Grupo'),
        ),
    ]
