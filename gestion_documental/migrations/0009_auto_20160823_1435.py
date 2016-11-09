# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_documental', '0008_auto_20160719_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudcustodiadocumento',
            name='estado',
            field=models.CharField(default='PE', verbose_name='Estado', choices=[('PE', 'PENDIENTE'), ('RE', 'REALIZADO'), ('PR', 'PROCESO')], max_length=2),
        ),
    ]
