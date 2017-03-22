# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
        ('gestion_documental', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipodocumento',
            name='areas',
            field=models.ManyToManyField(to='organizacional.Area', verbose_name='áreas', related_name='tipos_documento'),
        ),
        migrations.AddField(
            model_name='solicitudregistro',
            name='registro',
            field=models.ForeignKey(to='gestion_documental.Registro', verbose_name='Registro'),
        ),
        migrations.AddField(
            model_name='solicitudregistro',
            name='usuario_autoriza',
            field=models.ForeignKey(to='organizacional.Empleado', blank=True, related_name='autorizaciones', verbose_name='Autoriza', null=True),
        ),
        migrations.AddField(
            model_name='solicitudregistro',
            name='usuario_solicita',
            field=models.ForeignKey(to='organizacional.Empleado', verbose_name='Solicitante', related_name='solicitudes'),
        ),
        migrations.AddField(
            model_name='solicitudcustodiadocumento',
            name='area',
            field=models.ForeignKey(to='organizacional.Area', verbose_name='Área'),
        ),
        migrations.AddField(
            model_name='solicitudcustodiadocumento',
            name='solicitante',
            field=models.ForeignKey(to='organizacional.Empleado', verbose_name='Solicitante', related_name='solicitudes_custodia'),
        ),
        migrations.AddField(
            model_name='solicitudcustodiadocumento',
            name='tipo_documento',
            field=models.ForeignKey(to='gestion_documental.TipoDocumento', verbose_name='Tipo de Documento'),
        ),
        migrations.AddField(
            model_name='solicitudcustodiadocumento',
            name='usuario_recibe',
            field=models.ForeignKey(to='organizacional.Empleado', verbose_name='Usuario Recibe Documento', related_name='solicitudes_custodia_recibidas'),
        ),
        migrations.AddField(
            model_name='registro',
            name='area',
            field=models.ForeignKey(to='organizacional.Area', verbose_name='área', related_name='registros'),
        ),
        migrations.AddField(
            model_name='registro',
            name='modificado_por',
            field=models.ForeignKey(to='organizacional.Empleado', blank=True, verbose_name='Modificado Por', null=True),
        ),
        migrations.AddField(
            model_name='registro',
            name='palabras_claves',
            field=models.ManyToManyField(to='gestion_documental.PalabraClave', blank=True, related_name='registros', verbose_name='palabras claves'),
        ),
        migrations.AddField(
            model_name='documento',
            name='registro',
            field=models.ForeignKey(to='gestion_documental.Registro', verbose_name='registro', related_name='documentos'),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo_documento',
            field=models.ForeignKey(to='gestion_documental.TipoDocumento', verbose_name='tipo de documento', related_name='documentos'),
        ),
    ]
