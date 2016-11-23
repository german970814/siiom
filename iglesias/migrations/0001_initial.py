# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Iglesia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=200)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='fecha de registro')),
            ],
            options={
                'verbose_name': 'iglesia',
                'verbose_name_plural': 'iglesias',
            },
        ),
    ]
