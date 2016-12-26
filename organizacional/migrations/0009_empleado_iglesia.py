# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iglesias', '0001_initial'),
        ('organizacional', '0008_empleado_cargo'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='iglesia',
            field=models.ForeignKey(related_name='empleados', null=True, to='iglesias.Iglesia', verbose_name='iglesia'),
        ),
    ]
