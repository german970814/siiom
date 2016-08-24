# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import gestion_documental.models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacional', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('archivo', models.FileField(verbose_name='archivo', upload_to=gestion_documental.models.Documento.ruta_archivo)),
            ],
            options={
                'verbose_name_plural': 'documentos',
                'verbose_name': 'documento',
            },
        ),
        migrations.CreateModel(
            name='PalabraClave',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=250)),
            ],
            options={
                'verbose_name_plural': 'palabras claves',
                'verbose_name': 'palabra clave',
            },
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.TextField(verbose_name='descripción')),
                ('area', models.ForeignKey(verbose_name='área', related_name='registros', to='organizacional.Area')),
                ('palabras_claves', models.ManyToManyField(to='gestion_documental.PalabraClave', verbose_name='palabras claves', blank=True, related_name='registros')),
            ],
            options={
                'verbose_name_plural': 'registros',
                'verbose_name': 'registro',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=100)),
                ('areas', models.ManyToManyField(to='organizacional.Area', verbose_name='áreas', related_name='tipos_documento')),
            ],
            options={
                'verbose_name_plural': 'tipos de documento',
                'verbose_name': 'tipo de documento',
            },
        ),
        migrations.AddField(
            model_name='documento',
            name='registro',
            field=models.ForeignKey(verbose_name='registro', related_name='documentos', to='gestion_documental.Registro'),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo_documento',
            field=models.ForeignKey(verbose_name='tipo de documento', related_name='documentos', to='gestion_documental.TipoDocumento'),
        ),
    ]
