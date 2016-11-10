# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pqr.models


class Migration(migrations.Migration):

    dependencies = [
        ('pqr', '0003_caso_fecha_ingreso_habil'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('archivo', models.FileField(upload_to=pqr.models.Documento.ruta_archivo, verbose_name='Archivo')),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='documento',
            field=models.BooleanField(verbose_name='documento', default=False),
        ),
        migrations.AlterField(
            model_name='caso',
            name='telefono',
            field=models.BigIntegerField(verbose_name='teléfono', default=3593410),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documento',
            name='caso',
            field=models.ForeignKey(verbose_name='Caso', to='pqr.Caso'),
        ),
    ]
