# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0002_auto_20160201_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='diaDiscipulado',
            field=models.CharField(verbose_name='Dia Discipulado', max_length=1, null=True, choices=[('0', 'Lunes'), ('1', 'Martes'), ('2', 'Miercoles'), ('3', 'Jueves'), ('4', 'Viernes'), ('5', 'Sabado'), ('6', 'Domingo')], blank=True),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='horaDiscipulado',
            field=models.TimeField(verbose_name='Hora Discipulado', null=True, blank=True),
        ),
    ]
