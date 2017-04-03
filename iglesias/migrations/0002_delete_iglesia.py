# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iglesias', '0001_initial'),
        ('grupos', '0004_remove_grupo_iglesia'),
        ('miembros', '0002_remove_miembro_iglesia'),
        ('organizacional', '0002_remove_empleado_iglesia'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Iglesia',
        ),
    ]
