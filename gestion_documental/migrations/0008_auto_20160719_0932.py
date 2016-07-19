# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0003_auto_20160713_1553'),
        ('gestion_documental', '0007_solicitudcustodiadocumento'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='modificado_por',
            field=models.ForeignKey(blank=True, null=True, to='organizacional.Empleado', verbose_name='Modificado Por'),
        ),
        migrations.AddField(
            model_name='registro',
            name='ultima_modificacion',
            field=models.DateField(blank=True, verbose_name='Fecha Última Modificación', null=True),
        ),
    ]
