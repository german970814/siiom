# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0005_requisicion_estado_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='asunto',
            field=models.CharField(max_length=255, verbose_name='asunto', default='ASUNTO DE REQUISICIONES'),
            preserve_default=False,
        ),
    ]
