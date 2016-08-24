# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0003_auto_20160713_1553'),
        ('gestion_documental', '0006_auto_20160714_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudCustodiaDocumento',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('fecha_solicitud', models.DateField(auto_now_add=True, verbose_name='Fecha Solicitud')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('estado', models.CharField(default='PE', max_length=2, verbose_name='Estado', choices=[('PE', 'PENDIENTE'), ('RE', 'REALIZADO')])),
                ('area', models.ForeignKey(to='organizacional.Area', verbose_name='Área')),
                ('solicitante', models.ForeignKey(related_name='solicitudes_custodia', to='organizacional.Empleado', verbose_name='Solicitante')),
                ('tipo_documento', models.ForeignKey(to='gestion_documental.TipoDocumento', verbose_name='Tipo de Documento')),
                ('usuario_recibe', models.ForeignKey(related_name='solicitudes_custodia_recibidas', to='organizacional.Empleado', verbose_name='Usuario Recibe Documento')),
            ],
        ),
    ]
