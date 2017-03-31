# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tenant_schemas.postgresql_backend.base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Iglesia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('domain_url', models.CharField(unique=True, max_length=128)),
                ('schema_name', models.CharField(unique=True, max_length=63, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
                ('nombre', models.CharField(max_length=200, verbose_name='nombre')),
                ('creada_el', models.DateTimeField(verbose_name='creada el', auto_now_add=True)),
                ('logo', models.ImageField(blank=True, upload_to='', verbose_name='logo', null=True)),
                ('termino_gar', models.CharField(max_length=100, verbose_name='termino GAR', default='GAR')),
                ('termino_visitas', models.CharField(max_length=100, verbose_name='termino visitas', default='visitas')),
            ],
            options={
                'verbose_name': 'iglesia',
                'verbose_name_plural': 'iglesias',
            },
        ),
    ]
