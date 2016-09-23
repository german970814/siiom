# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0005_llenar_padre_grupo_20160824_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='lider1',
            field=models.ForeignKey(related_name='lider_uno', blank=True, null=True, to='miembros.Miembro'),
        ),
    ]
