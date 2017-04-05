# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
from django.conf import settings
import miembros.models
import common.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grupos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CambioTipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=30, verbose_name='nombre')),
                ('primer_apellido', models.CharField(max_length=20, verbose_name='primer apellido')),
                ('segundo_apellido', models.CharField(blank=True, null=True, max_length=20, verbose_name='segundo apellido')),
                ('genero', models.CharField(max_length=1, choices=[('F', 'Femenino'), ('M', 'Masculino')], verbose_name='género')),
                ('telefono', models.CharField(blank=True, null=True, max_length=50, verbose_name='teléfono')),
                ('celular', models.CharField(blank=True, null=True, max_length=50, verbose_name='celular')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')),
                ('cedula', models.CharField(validators=[django.core.validators.RegexValidator('^[0-9]+$', 'Se aceptan solo numeros')], max_length=25, unique=True, verbose_name='cédula')),
                ('direccion', models.CharField(blank=True, null=True, max_length=50, verbose_name='dirección')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('profesion', models.CharField(blank=True, null=True, max_length=20, verbose_name='profesion')),
                ('estado_civil', models.CharField(blank=True, null=True, max_length=1, choices=[('V', 'Viudo'), ('C', 'Casado'), ('S', 'Soltero'), ('D', 'Divorciado')], verbose_name='estado civil')),
                ('foto_perfil', models.ImageField(upload_to=miembros.models.Miembro.ruta_imagen, blank=True, null=True, verbose_name='foto perfil')),
                ('portada', models.ImageField(upload_to=miembros.models.Miembro.ruta_imagen, blank=True, null=True, verbose_name='portada')),
                ('estado', models.CharField(max_length=1, choices=[('A', 'Activo'), ('I', 'Inactivo'), ('R', 'Restauración')], verbose_name='estado')),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='fecha de registro')),
                ('barrio', models.ForeignKey(verbose_name='barrio', blank=True, to='miembros.Barrio', null=True)),
                ('conyugue', models.ForeignKey(related_name='casado_con', verbose_name='cónyugue', blank=True, to='miembros.Miembro', null=True)),
                ('grupo', models.ForeignKey(related_name='miembros', verbose_name='grupo', blank=True, to='grupos.Grupo', null=True)),
                ('grupo_lidera', models.ForeignKey(related_name='lideres', verbose_name='grupo que lidera', blank=True, to='grupos.Grupo', null=True)),
                ('usuario', models.ForeignKey(verbose_name='usuario', blank=True, to=settings.AUTH_USER_MODEL, unique=True, null=True)),
            ],
            options={
                'permissions': (('es_agente', 'define si un miembro es agente'), ('es_lider', 'indica si el usuario es lider de un GAR'), ('es_administrador', 'es adminisitrador'), ('es_pastor', 'indica si un miembro es pastor'), ('es_tesorero', 'indica si un miembro es tesorero'), ('es_coordinador', 'indica si un miembro es coordinador'), ('buscar_todos', 'indica si un usuario puede buscar miembros')),
            },
            bases=(common.models.UtilsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TipoMiembro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='cambiotipo',
            name='anteriorTipo',
            field=models.ForeignKey(related_name='tipo_anterior', verbose_name='tipo anterior', to='miembros.TipoMiembro', null=True),
        ),
        migrations.AddField(
            model_name='cambiotipo',
            name='autorizacion',
            field=models.ForeignKey(to='miembros.Miembro', related_name='miembro_autoriza'),
        ),
        migrations.AddField(
            model_name='cambiotipo',
            name='miembro',
            field=models.ForeignKey(to='miembros.Miembro', related_name='miembro_cambiado'),
        ),
        migrations.AddField(
            model_name='cambiotipo',
            name='nuevoTipo',
            field=models.ForeignKey(verbose_name='tipo nuevo', to='miembros.TipoMiembro', related_name='tipo_nuevo'),
        ),
        migrations.AddField(
            model_name='barrio',
            name='zona',
            field=models.ForeignKey(to='miembros.Zona'),
        ),
    ]
