# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import miembros.models
import common.models
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iglesias', '0001_initial'),
        ('grupos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CambioTipo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(verbose_name='nombre', max_length=30)),
                ('primer_apellido', models.CharField(verbose_name='primer apellido', max_length=20)),
                ('segundo_apellido', models.CharField(blank=True, max_length=20, null=True, verbose_name='segundo apellido')),
                ('genero', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], verbose_name='género', max_length=1)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True, verbose_name='teléfono')),
                ('celular', models.CharField(blank=True, max_length=50, null=True, verbose_name='celular')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')),
                ('cedula', models.CharField(verbose_name='cédula', max_length=25, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]+$', 'Se aceptan solo numeros')])),
                ('direccion', models.CharField(blank=True, max_length=50, null=True, verbose_name='dirección')),
                ('email', models.EmailField(verbose_name='email', max_length=254, unique=True)),
                ('profesion', models.CharField(blank=True, max_length=20, null=True, verbose_name='profesion')),
                ('estado_civil', models.CharField(choices=[('V', 'Viudo'), ('C', 'Casado'), ('S', 'Soltero'), ('D', 'Divorciado')], blank=True, max_length=1, null=True, verbose_name='estado civil')),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to=miembros.models.Miembro.ruta_imagen, verbose_name='foto perfil')),
                ('portada', models.ImageField(blank=True, null=True, upload_to=miembros.models.Miembro.ruta_imagen, verbose_name='portada')),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo'), ('R', 'Restauración')], verbose_name='estado', max_length=1)),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='fecha de registro')),
                ('barrio', models.ForeignKey(to='miembros.Barrio', blank=True, verbose_name='barrio', null=True)),
                ('conyugue', models.ForeignKey(to='miembros.Miembro', blank=True, related_name='casado_con', verbose_name='cónyugue', null=True)),
                ('grupo', models.ForeignKey(to='grupos.Grupo', blank=True, related_name='miembros', verbose_name='grupo', null=True)),
                ('grupo_lidera', models.ForeignKey(to='grupos.Grupo', blank=True, related_name='lideres', verbose_name='grupo que lidera', null=True)),
                ('iglesia', models.ForeignKey(to='iglesias.Iglesia', verbose_name='iglesia')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, unique=True, verbose_name='usuario', null=True)),
            ],
            options={
                'permissions': (('es_agente', 'define si un miembro es agente'), ('es_lider', 'indica si el usuario es lider de un GAR'), ('es_administrador', 'es adminisitrador'), ('es_pastor', 'indica si un miembro es pastor'), ('es_tesorero', 'indica si un miembro es tesorero'), ('es_coordinador', 'indica si un miembro es coordinador'), ('buscar_todos', 'indica si un usuario puede buscar miembros')),
            },
            bases=(common.models.UtilsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TipoMiembro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='cambiotipo',
            name='anteriorTipo',
            field=models.ForeignKey(to='miembros.TipoMiembro', verbose_name='tipo anterior', related_name='tipo_anterior', null=True),
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
            field=models.ForeignKey(to='miembros.TipoMiembro', verbose_name='tipo nuevo', related_name='tipo_nuevo'),
        ),
        migrations.AddField(
            model_name='barrio',
            name='zona',
            field=models.ForeignKey(to='miembros.Zona'),
        ),
    ]
