# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0016_auto_20161121_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='fecha_proyeccion',
            field=models.DateField(verbose_name='fecha proyección pago', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='requisicion',
            name='fecha_solicitud',
            field=models.DateField(verbose_name='fecha solicitud recurso', null=True, blank=True),
        ),
    ]
