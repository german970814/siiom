# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0016_auto_20170103_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialEstado',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('fecha', models.DateTimeField(verbose_name='fecha')),
                ('estado', models.CharField(verbose_name='estado', max_length=2, choices=[('AC', 'ACTIVO'), ('IN', 'INACTIVO'), ('SU', 'SUSPENDIDO'), ('AR', 'ARCHIVADO')])),
                ('grupo', models.ForeignKey(related_name='historiales', to='grupos.Grupo', verbose_name='grupo')),
            ],
        ),
    ]
