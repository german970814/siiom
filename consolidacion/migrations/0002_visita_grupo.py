# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consolidacion', '0001_initial'),
        ('grupos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visita',
            name='grupo',
            field=models.ForeignKey(related_name='visitas', verbose_name='grupo', blank=True, to='grupos.Grupo', null=True),
        ),
    ]
