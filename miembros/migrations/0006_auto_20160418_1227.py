# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import miembros.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0005_auto_20160317_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='foto_perfil',
            field=models.ImageField(null=True, upload_to=miembros.models.Miembro.ruta_imagen, blank=True),
        ),
        migrations.AddField(
            model_name='miembro',
            name='portada',
            field=models.ImageField(null=True, upload_to=miembros.models.Miembro.ruta_imagen, blank=True),
        ),
        migrations.AlterField(
            model_name='cambioescalafon',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 4, 18, 12, 27, 7, 808960)),
        ),
    ]
