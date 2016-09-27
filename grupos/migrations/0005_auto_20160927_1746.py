# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0004_reuniongar_digitada_por_miembro'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='parent',
            field=models.ForeignKey(null=True, to='grupos.Grupo', related_name='children_set'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='lider1',
            field=models.ForeignKey(blank=True, null=True, to='miembros.Miembro', related_name='lider_uno'),
        ),
    ]
