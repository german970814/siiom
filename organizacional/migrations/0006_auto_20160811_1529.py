# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0005_auto_20160803_1516'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empleado',
            options={'verbose_name': 'empleado', 'verbose_name_plural': 'empleados', 'permissions': (('es_administrador_sgd', 'Es Administrador de Sistema Gestion Documental'), ('buscar_registros', 'Puede Buscar Registros'), ('es_compras', 'Es usuario de compras'), ('es_presidente', 'Es presidente'))},
        ),
    ]
