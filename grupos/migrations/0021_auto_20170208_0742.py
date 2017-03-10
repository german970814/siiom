# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0020_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historialestado',
            options={'verbose_name': 'Historial', 'verbose_name_plural': 'Historiales', 'ordering': ['-fecha']},
        ),
        migrations.RemoveField(
            model_name='grupo',
            name='estado',
        ),
        migrations.AlterField(
            model_name='grupo',
            name='nombre',
            field=models.CharField(verbose_name='nombre', max_length=255),
        ),
    ]
