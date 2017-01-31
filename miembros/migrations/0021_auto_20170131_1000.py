# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0020_auto_20161228_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembro',
            name='grupo',
            field=models.ForeignKey(verbose_name='grupo', null=True, related_name='miembros', blank=True, to='grupos.Grupo'),
        ),
    ]
