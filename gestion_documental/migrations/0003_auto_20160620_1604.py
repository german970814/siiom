# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_documental', '0002_registro_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palabraclave',
            name='nombre',
            field=models.CharField(verbose_name='nombre', max_length=250, unique=True),
        ),
    ]
