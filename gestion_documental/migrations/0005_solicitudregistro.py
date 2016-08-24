# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0003_auto_20160713_1553'),
        ('gestion_documental', '0004_auto_20160713_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudRegistro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('estado', models.CharField(verbose_name='Estado Solicitud', max_length=2, choices=[('PE', 'PENDIENTE'), ('ED', 'ENTREGADO POR DIGITADOR'), ('DC', 'DEVUELTO POR USUARIO DE CONSULTA')])),
                ('fecha_solicitud', models.DateField(verbose_name='Fecha Solicitud', auto_now=True)),
                ('fecha_devolucion', models.DateField(verbose_name='Fecha Devolución', blank=True)),
                ('comentario', models.TextField(verbose_name='Comentario', blank=True)),
                ('registro', models.ForeignKey(verbose_name='Registro', to='gestion_documental.Registro')),
                ('usuario_autoriza', models.ForeignKey(null=True, related_name='autorizaciones', verbose_name='Autoriza', blank=True, to='organizacional.Empleado')),
                ('usuario_solicita', models.ForeignKey(related_name='solicitudes', verbose_name='Solicitante', to='organizacional.Empleado')),
            ],
            options={
                'verbose_name_plural': 'Solicitudes de Registro',
                'verbose_name': 'Solicitud de Registro',
            },
        ),
    ]
