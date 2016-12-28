# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import miembros.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0018_auto_20161124_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembro',
            name='barrio',
            field=models.ForeignKey(verbose_name='barrio', blank=True, to='miembros.Barrio', null=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='celular',
            field=models.CharField(verbose_name='celular', blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='convertido',
            field=models.BooleanField(verbose_name='convertido', default=False),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='email',
            field=models.EmailField(verbose_name='email', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='escalafon',
            field=models.ManyToManyField(verbose_name='escalafón', to='miembros.Escalafon', through='miembros.CambioEscalafon'),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='estado',
            field=models.CharField(verbose_name='estado', max_length=1, choices=[('A', 'Activo'), ('I', 'Inactivo'), ('R', 'Restauración')]),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='estadoCivil',
            field=models.CharField(verbose_name='estado civil', blank=True, max_length=1, choices=[('V', 'Viudo'), ('C', 'Casado'), ('S', 'Soltero'), ('D', 'Divorciado')], null=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='fechaRegistro',
            field=models.DateField(verbose_name='fecha de registro', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='foto_perfil',
            field=models.ImageField(verbose_name='foto perfil', blank=True, upload_to=miembros.models.Miembro.ruta_imagen, null=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='genero',
            field=models.CharField(verbose_name='género', max_length=1, choices=[('F', 'Femenino'), ('M', 'Masculino')]),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='grupo',
            field=models.ForeignKey(verbose_name='grupo', blank=True, to='grupos.Grupo', null=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='nombre',
            field=models.CharField(verbose_name='nombre', max_length=30),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='pasos',
            field=models.ManyToManyField(verbose_name='pasos', blank=True, to='miembros.Pasos', through='miembros.CumplimientoPasos'),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='portada',
            field=models.ImageField(verbose_name='portada', blank=True, upload_to=miembros.models.Miembro.ruta_imagen, null=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='profesion',
            field=models.CharField(verbose_name='profesion', blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='usuario',
            field=models.ForeignKey(verbose_name='usuario', blank=True, unique=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
