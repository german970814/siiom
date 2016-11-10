# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_auto_20160803_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='fecha_pago',
            field=models.DateField(blank=True, null=True, verbose_name='fecha de pago'),
        ),
        migrations.AddField(
            model_name='requisicion',
            name='form_pago',
            field=models.CharField(blank=True, verbose_name='forma de pago', max_length=1, choices=[('E', 'EFECTIVO'), ('C', 'CRÉDITO')]),
        ),
        migrations.AlterField(
            model_name='requisicion',
            name='estado',
            field=models.CharField(default='PE', verbose_name='estado', max_length=2, choices=[('PE', 'PENDIENTE'), ('PR', 'PROCESO'), ('TE', 'TERMINADA'), ('AN', 'RECHAZADA')]),
        ),
    ]
