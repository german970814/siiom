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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_url', models.CharField(unique=True, max_length=128)),
                ('schema_name', models.CharField(validators=[tenant_schemas.postgresql_backend.base._check_schema_name], unique=True, max_length=63)),
                ('nombre', models.CharField(max_length=200, verbose_name='nombre')),
                ('creada_el', models.DateTimeField(auto_now_add=True, verbose_name='creada el')),
            ],
            options={
                'verbose_name_plural': 'iglesias',
                'verbose_name': 'iglesia',
            },
        ),
    ]
