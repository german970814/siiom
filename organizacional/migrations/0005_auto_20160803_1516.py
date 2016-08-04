# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0004_empleado_jefe_departamento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empleado',
            options={'verbose_name': 'empleado', 'permissions': (('es_administrador_sgd', 'Es Administrador de Sistema Gestion Documental'), ('buscar_registros', 'Puede Buscar Registros'), ('es_compras', 'Es usuario de compras')), 'verbose_name_plural': 'empleados'},
        ),
    ]
