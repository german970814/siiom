# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empleado',
            options={'permissions': (('es_administrador_sgd', 'Es Administrador de Sistema Gestion Documental'), ('buscar_registros', 'Puede Buscar Registros')), 'verbose_name_plural': 'empleados', 'verbose_name': 'empleado'},
        ),
    ]
