# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuentros', '0001_initial'),
        ('miembros', '0001_initial'),
        ('grupos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentro',
            name='coordinador',
            field=models.ForeignKey(to='miembros.Miembro', verbose_name='Coordinador', related_name='encuentros_coordinador'),
        ),
        migrations.AddField(
            model_name='encuentro',
            name='grupos',
            field=models.ManyToManyField(to='grupos.Grupo', verbose_name='Grupos'),
        ),
        migrations.AddField(
            model_name='encuentro',
            name='tesorero',
            field=models.ForeignKey(to='miembros.Miembro', verbose_name='Tesorero', related_name='encuentros_tesorero'),
        ),
        migrations.AddField(
            model_name='encontrista',
            name='encuentro',
            field=models.ForeignKey(to='encuentros.Encuentro', verbose_name='Encuentro'),
        ),
        migrations.AddField(
            model_name='encontrista',
            name='grupo',
            field=models.ForeignKey(to='grupos.Grupo', verbose_name='Grupo', related_name='encontristas'),
        ),
    ]
