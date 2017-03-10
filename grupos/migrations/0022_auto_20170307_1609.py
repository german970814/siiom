# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0021_auto_20170208_0742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistenciamiembro',
            name='miembro',
        ),
        migrations.RemoveField(
            model_name='asistenciamiembro',
            name='reunion',
        ),
        migrations.RemoveField(
            model_name='reuniondiscipulado',
            name='asistentecia',
        ),
        migrations.RemoveField(
            model_name='reuniongar',
            name='asistentecia',
        ),
        migrations.DeleteModel(
            name='AsistenciaMiembro',
        ),
    ]
