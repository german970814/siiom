# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_documental', '0005_solicitudregistro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudregistro',
            name='fecha_devolucion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Devolución'),
        ),
        migrations.AlterField(
            model_name='solicitudregistro',
            name='fecha_solicitud',
            field=models.DateField(auto_now_add=True, verbose_name='Fecha Solicitud'),
        ),
    ]
