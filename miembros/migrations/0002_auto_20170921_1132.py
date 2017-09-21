# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Escalafon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(verbose_name='nombre', max_length=200)),
                ('cantidad_grupos', models.IntegerField(verbose_name='cantidad grupos')),
            ],
        ),
        migrations.AddField(
            model_name='miembro',
            name='talla',
            field=models.CharField(verbose_name='talla', max_length=5, blank=True),
        ),
        migrations.AddField(
            model_name='miembro',
            name='escalafon',
            field=models.ForeignKey(verbose_name='escalafon', blank=True, null=True, related_name='lideres', to='miembros.Escalafon'),
        ),
    ]
