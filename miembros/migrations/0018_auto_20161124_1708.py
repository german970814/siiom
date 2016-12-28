# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0017_asignar_iglesia_20161124_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembro',
            name='iglesia',
            field=models.ForeignKey(related_name='miembros', to='iglesias.Iglesia', verbose_name='iglesia'),
        ),
    ]
