# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0021_auto_20170131_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='miembro',
            name='asignadoGAR',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='asisteGAR',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='detalleLlamadaLider',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='detallePrimeraLlamada',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='detalleSegundaLlamada',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='fechaAsignacionGAR',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='fechaLlamadaLider',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='fechaPrimeraLlamada',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='fechaSegundaLlamada',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='noInteresadoGAR',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='observacionLlamadaLider',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='observacionPrimeraLlamada',
        ),
        migrations.RemoveField(
            model_name='miembro',
            name='observacionSegundaLlamada',
        ),
    ]
