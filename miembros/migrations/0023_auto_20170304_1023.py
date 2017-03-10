# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0022_auto_20170304_1012'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DetalleLlamada',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='convertido',
        ),
    ]
