# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0001_initial'),
        ('miembros', '0001_initial'),
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
            field=models.ForeignKey(verbose_name='grupo', to='grupos.Grupo', related_name='historiales'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='barrio',
            field=models.ForeignKey(to='miembros.Barrio', verbose_name='barrio'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='parent',
            field=models.ForeignKey(related_name='children_set', verbose_name='grupo origen', to='grupos.Grupo', null=True),
        ),
        migrations.AddField(
            model_name='grupo',
            name='red',
            field=models.ForeignKey(verbose_name='red', blank=True, to='grupos.Red', null=True),
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
