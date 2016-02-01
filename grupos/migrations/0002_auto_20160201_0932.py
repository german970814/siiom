# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0001_initial'),
        ('grupos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reuniongar',
            name='asistentecia',
            field=models.ManyToManyField(to='miembros.Miembro', through='grupos.AsistenciaMiembro'),
        ),
        migrations.AddField(
            model_name='reuniongar',
            name='grupo',
            field=models.ForeignKey(to='grupos.Grupo'),
        ),
        migrations.AddField(
            model_name='reuniondiscipulado',
            name='asistentecia',
            field=models.ManyToManyField(to='miembros.Miembro', through='grupos.AsistenciaDiscipulado'),
        ),
        migrations.AddField(
            model_name='reuniondiscipulado',
            name='grupo',
            field=models.ForeignKey(to='grupos.Grupo'),
        ),
        migrations.AddField(
            model_name='reuniondiscipulado',
            name='predica',
            field=models.ForeignKey(verbose_name='prédica', to='grupos.Predica'),
        ),
        migrations.AddField(
            model_name='predica',
            name='miembro',
            field=models.ForeignKey(to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='barrio',
            field=models.ForeignKey(to='miembros.Barrio'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='lider1',
            field=models.ForeignKey(to='miembros.Miembro', related_name='lider_uno'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='lider2',
            field=models.ForeignKey(blank=True, related_name='lider_dos', to='miembros.Miembro', null=True),
        ),
        migrations.AddField(
            model_name='grupo',
            name='red',
            field=models.ForeignKey(blank=True, to='grupos.Red', null=True),
        ),
        migrations.AddField(
            model_name='asistenciamiembro',
            name='miembro',
            field=models.ForeignKey(to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='asistenciamiembro',
            name='reunion',
            field=models.ForeignKey(to='grupos.ReunionGAR'),
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
