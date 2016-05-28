# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0009_eliminar_usuarios_no_asignados_a_miembros_20160430_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cambioescalafon',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 5, 25, 15, 25, 35, 926885)),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='cedula',
            field=models.CharField(verbose_name='cédula', max_length=25, validators=[django.core.validators.RegexValidator('^[0-9]+$', 'Se aceptan solo numeros')], unique=True),
        ),
    ]
