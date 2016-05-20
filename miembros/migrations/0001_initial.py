# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CambioEscalafon',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateField(default=datetime.datetime(2016, 2, 1, 9, 32, 44, 85799))),
            ],
        ),
        migrations.CreateModel(
            name='CambioTipo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CumplimientoPasos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleLlamada',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Escalafon',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('celulas', models.PositiveIntegerField()),
                ('descripcion', models.TextField(max_length=200)),
                ('logro', models.TextField(max_length=200)),
                ('rango', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=30)),
                ('primerApellido', models.CharField(max_length=20, verbose_name='primer apellido')),
                ('segundoApellido', models.CharField(max_length=20, verbose_name='segundo apellido', null=True, blank=True)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, verbose_name='género')),
                ('telefono', models.CharField(max_length=50, verbose_name='teléfono', null=True, blank=True)),
                ('celular', models.CharField(max_length=50, blank=True, null=True)),
                ('fechaNacimiento', models.DateField(blank=True, verbose_name='fecha de nacimiento', null=True)),
                ('cedula', models.CharField(max_length=25, verbose_name='cédula', unique=True)),
                ('direccion', models.CharField(max_length=50, verbose_name='dirección', null=True, blank=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('profesion', models.CharField(max_length=20, verbose_name='profesión', null=True, blank=True)),
                ('estadoCivil', models.CharField(choices=[('C', 'Casado'), ('S', 'Soltero'), ('V', 'Viudo'), ('D', 'Divorciado')], max_length=1, verbose_name='estado civil', null=True, blank=True)),
                ('convertido', models.BooleanField(default=False)),
                ('estado', models.CharField(choices=[('A', 'Activo'), ('I', 'Inactivo'), ('R', 'Restauración')], max_length=1)),
                ('asignadoGAR', models.BooleanField(verbose_name='asignado a GAR', default=False)),
                ('asisteGAR', models.BooleanField(verbose_name='asiste a GAR', default=False)),
                ('noInteresadoGAR', models.BooleanField(verbose_name='no interesado en GAR', default=False)),
                ('fechaAsignacionGAR', models.DateField(blank=True, verbose_name='fecha de asignación a GAR', null=True)),
                ('fechaLlamadaLider', models.DateField(blank=True, verbose_name='fecha de llamada del líder', null=True)),
                ('observacionLlamadaLider', models.TextField(max_length=300, verbose_name='observación de llamada del líder', null=True, blank=True)),
                ('fechaPrimeraLlamada', models.DateField(blank=True, verbose_name='fecha de primera llamada', null=True)),
                ('observacionPrimeraLlamada', models.TextField(max_length=300, verbose_name='observación de primera llamada', null=True, blank=True)),
                ('fechaSegundaLlamada', models.DateField(blank=True, verbose_name='fecha de segunda llamada', null=True)),
                ('observacionSegundaLlamada', models.TextField(max_length=300, verbose_name='observación de segunda llamada', null=True, blank=True)),
                ('fechaRegistro', models.DateField(auto_now_add=True)),
                ('barrio', models.ForeignKey(blank=True, to='miembros.Barrio', null=True)),
                ('conyugue', models.ForeignKey(to='miembros.Miembro', related_name='casado_con', blank=True, null=True, verbose_name='cónyugue')),
                ('detalleLlamadaLider', models.ForeignKey(to='miembros.DetalleLlamada', related_name='llamada_lider', blank=True, null=True, verbose_name='detalle de llamada del líder')),
                ('detallePrimeraLlamada', models.ForeignKey(to='miembros.DetalleLlamada', related_name='primera_llamada', blank=True, null=True, verbose_name='detalle de primera llamada')),
                ('detalleSegundaLlamada', models.ForeignKey(to='miembros.DetalleLlamada', related_name='segunda_llamada', blank=True, null=True, verbose_name='detalle de segunda llamada')),
                ('escalafon', models.ManyToManyField(to='miembros.Escalafon', through='miembros.CambioEscalafon')),
                ('grupo', models.ForeignKey(blank=True, to='grupos.Grupo', null=True)),
            ],
            options={
                'permissions': (('es_agente', 'define si un miembro es agente'), ('es_lider', 'indica si el usuario es lider de un GAR'), ('es_maestro', 'indica si un usuario es maestro de un curso'), ('es_administrador', 'es adminisitrador'), ('buscar_todos', 'indica si un usuario puede buscar miembros'), ('puede_editar_miembro', 'indica si un usuario puede editar miembros'), ('puede_agregar_visitante', 'puede agregar miembros visitantes'), ('llamada_lider', 'puede modificar llamada lider'), ('llamada_agente', 'puede modificar llamada agente'), ('cumplimiento_pasos', 'puede registrar el cumplimiento de pasos'), ('es_pastor', 'indica si un miembro es pastor')),
            },
        ),
        migrations.CreateModel(
            name='Pasos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=20)),
                ('prioridad', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoMiembro',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='miembro',
            name='pasos',
            field=models.ManyToManyField(to='miembros.Pasos', blank=True, through='miembros.CumplimientoPasos'),
        ),
        migrations.AddField(
            model_name='miembro',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='cumplimientopasos',
            name='miembro',
            field=models.ForeignKey(to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='cumplimientopasos',
            name='paso',
            field=models.ForeignKey(to='miembros.Pasos'),
        ),
        migrations.AddField(
            model_name='cambiotipo',
            name='anteriorTipo',
            field=models.ForeignKey(related_name='tipo_anterior', to='miembros.TipoMiembro', null=True, verbose_name='tipo anterior'),
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
            field=models.ForeignKey(related_name='tipo_nuevo', to='miembros.TipoMiembro', verbose_name='tipo nuevo'),
        ),
        migrations.AddField(
            model_name='cambioescalafon',
            name='escalafon',
            field=models.ForeignKey(to='miembros.Escalafon'),
        ),
        migrations.AddField(
            model_name='cambioescalafon',
            name='miembro',
            field=models.ForeignKey(to='miembros.Miembro'),
        ),
        migrations.AddField(
            model_name='barrio',
            name='zona',
            field=models.ForeignKey(to='miembros.Zona'),
        ),
    ]
