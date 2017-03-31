# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0001_initial'),
        ('iglesias', '0001_initial'),
        ('grupos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='predica',
            name='miembro',
            field=models.ForeignKey(to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='historialestado',
            name='grupo',
            field=models.ForeignKey(to='grupos.Grupo', verbose_name='grupo', related_name='historiales'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='barrio',
            field=models.ForeignKey(to='miembros.Barrio', verbose_name='barrio'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='iglesia',
            field=models.ForeignKey(to='iglesias.Iglesia', verbose_name='iglesia'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='parent',
            field=models.ForeignKey(to='grupos.Grupo', verbose_name='grupo origen', related_name='children_set', null=True),
        ),
        migrations.AddField(
            model_name='grupo',
            name='red',
            field=models.ForeignKey(to='grupos.Red', blank=True, verbose_name='red', null=True),
        ),
        migrations.AddField(
            model_name='asistenciadiscipulado',
            name='miembro',
            field=models.ForeignKey(to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='asistenciadiscipulado',
            name='reunion',
            field=models.ForeignKey(to='grupos.ReunionDiscipulado'),
        ),
    ]
