# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0010_asignar_iglesia_20161203_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='iglesia',
            field=models.ForeignKey(to='iglesias.Iglesia', verbose_name='iglesia', related_name='empleados'),
        ),
    ]
