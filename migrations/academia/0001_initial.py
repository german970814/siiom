# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Modulo'
        db.create_table('academia_modulo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('porcentaje', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('academia', ['Modulo'])

        # Adding model 'Sesion'
        db.create_table('academia_sesion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('modulo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academia.Modulo'])),
        ))
        db.send_create_signal('academia', ['Sesion'])

        # Adding model 'Curso'
        db.create_table('academia_curso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('dia', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hora', self.gf('django.db.models.fields.TimeField')()),
            ('material', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('profesor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['miembros.Miembro'])),
            ('red', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grupos.Red'])),
        ))
        db.send_create_signal('academia', ['Curso'])

        # Adding M2M table for field modulos on 'Curso'
        m2m_table_name = db.shorten_name('academia_curso_modulos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('curso', models.ForeignKey(orm['academia.curso'], null=False)),
            ('modulo', models.ForeignKey(orm['academia.modulo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['curso_id', 'modulo_id'])

        # Adding model 'Matricula'
        db.create_table('academia_matricula', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fechaInicio', self.gf('django.db.models.fields.DateField')()),
            ('notaDefinitiva', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=3, decimal_places=2)),
            ('pago', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('estudiante', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['miembros.Miembro'], unique=True)),
            ('curso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academia.Curso'])),
            ('moduloActual', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='modulo_actual', null=True, to=orm['academia.Modulo'])),
        ))
        db.send_create_signal('academia', ['Matricula'])

        # Adding model 'AsistenciaSesiones'
        db.create_table('academia_asistenciasesiones', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('matricula', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academia.Matricula'])),
            ('sesion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academia.Sesion'])),
            ('asistencia', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tarea', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('academia', ['AsistenciaSesiones'])

        # Adding unique constraint on 'AsistenciaSesiones', fields ['matricula', 'sesion']
        db.create_unique('academia_asistenciasesiones', ['matricula_id', 'sesion_id'])

        # Adding model 'Reporte'
        db.create_table('academia_reporte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('matricula', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academia.Matricula'])),
            ('modulo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['academia.Modulo'])),
            ('nota', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal('academia', ['Reporte'])

        # Adding unique constraint on 'Reporte', fields ['matricula', 'modulo']
        db.create_unique('academia_reporte', ['matricula_id', 'modulo_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Reporte', fields ['matricula', 'modulo']
        db.delete_unique('academia_reporte', ['matricula_id', 'modulo_id'])

        # Removing unique constraint on 'AsistenciaSesiones', fields ['matricula', 'sesion']
        db.delete_unique('academia_asistenciasesiones', ['matricula_id', 'sesion_id'])

        # Deleting model 'Modulo'
        db.delete_table('academia_modulo')

        # Deleting model 'Sesion'
        db.delete_table('academia_sesion')

        # Deleting model 'Curso'
        db.delete_table('academia_curso')

        # Removing M2M table for field modulos on 'Curso'
        db.delete_table(db.shorten_name('academia_curso_modulos'))

        # Deleting model 'Matricula'
        db.delete_table('academia_matricula')

        # Deleting model 'AsistenciaSesiones'
        db.delete_table('academia_asistenciasesiones')

        # Deleting model 'Reporte'
        db.delete_table('academia_reporte')


    models = {
        'academia.asistenciasesiones': {
            'Meta': {'unique_together': "(('matricula', 'sesion'),)", 'object_name': 'AsistenciaSesiones'},
            'asistencia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academia.Matricula']"}),
            'sesion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academia.Sesion']"}),
            'tarea': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'academia.curso': {
            'Meta': {'object_name': 'Curso'},
            'dia': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'hora': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'modulos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['academia.Modulo']", 'symmetrical': 'False'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'profesor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Miembro']"}),
            'red': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grupos.Red']"})
        },
        'academia.matricula': {
            'Meta': {'object_name': 'Matricula'},
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academia.Curso']"}),
            'estudiante': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Miembro']", 'unique': 'True'}),
            'fechaInicio': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moduloActual': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'modulo_actual'", 'null': 'True', 'to': "orm['academia.Modulo']"}),
            'modulos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'reporte_modulo'", 'symmetrical': 'False', 'through': "orm['academia.Reporte']", 'to': "orm['academia.Modulo']"}),
            'notaDefinitiva': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '3', 'decimal_places': '2'}),
            'pago': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sesiones': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['academia.Sesion']", 'through': "orm['academia.AsistenciaSesiones']", 'symmetrical': 'False'})
        },
        'academia.modulo': {
            'Meta': {'object_name': 'Modulo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'porcentaje': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'academia.reporte': {
            'Meta': {'ordering': "['id']", 'unique_together': "(('matricula', 'modulo'),)", 'object_name': 'Reporte'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academia.Matricula']"}),
            'modulo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academia.Modulo']"}),
            'nota': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'})
        },
        'academia.sesion': {
            'Meta': {'object_name': 'Sesion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['academia.Modulo']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'grupos.grupo': {
            'Meta': {'object_name': 'Grupo'},
            'barrio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Barrio']"}),
            'diaDiscipulado': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'diaGAR': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'fechaApertura': ('django.db.models.fields.DateField', [], {}),
            'horaDiscipulado': ('django.db.models.fields.TimeField', [], {}),
            'horaGAR': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lider1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lider_uno'", 'to': "orm['miembros.Miembro']"}),
            'lider2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lider_dos'", 'null': 'True', 'to': "orm['miembros.Miembro']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'red': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grupos.Red']", 'null': 'True', 'blank': 'True'})
        },
        'grupos.red': {
            'Meta': {'object_name': 'Red'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'miembros.barrio': {
            'Meta': {'object_name': 'Barrio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zona': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Zona']"})
        },
        'miembros.cambioescalafon': {
            'Meta': {'object_name': 'CambioEscalafon'},
            'escalafon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Escalafon']"}),
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 1, 25, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miembro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Miembro']"})
        },
        'miembros.cumplimientopasos': {
            'Meta': {'object_name': 'CumplimientoPasos'},
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miembro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Miembro']"}),
            'paso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Pasos']"})
        },
        'miembros.detallellamada': {
            'Meta': {'object_name': 'DetalleLlamada'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'miembros.escalafon': {
            'Meta': {'object_name': 'Escalafon'},
            'celulas': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logro': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'rango': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'miembros.miembro': {
            'Meta': {'object_name': 'Miembro'},
            'asignadoGAR': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'asisteGAR': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'barrio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Barrio']", 'null': 'True', 'blank': 'True'}),
            'cedula': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'celular': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'convertido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'conyugue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'casado_con'", 'null': 'True', 'to': "orm['miembros.Miembro']"}),
            'detalleLlamadaLider': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'llamada_lider'", 'null': 'True', 'to': "orm['miembros.DetalleLlamada']"}),
            'detallePrimeraLlamada': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primera_llamada'", 'null': 'True', 'to': "orm['miembros.DetalleLlamada']"}),
            'detalleSegundaLlamada': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'segunda_llamada'", 'null': 'True', 'to': "orm['miembros.DetalleLlamada']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'escalafon': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['miembros.Escalafon']", 'through': "orm['miembros.CambioEscalafon']", 'symmetrical': 'False'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'estadoCivil': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'fechaAsignacionGAR': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fechaLlamadaLider': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fechaNacimiento': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fechaPrimeraLlamada': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fechaRegistro': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fechaSegundaLlamada': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'genero': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grupos.Grupo']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'noInteresadoGAR': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'observacionLlamadaLider': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'observacionPrimeraLlamada': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'observacionSegundaLlamada': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'pasos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['miembros.Pasos']", 'symmetrical': 'False', 'through': "orm['miembros.CumplimientoPasos']", 'blank': 'True'}),
            'primerApellido': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'profesion': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'segundoApellido': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'miembros.pasos': {
            'Meta': {'object_name': 'Pasos'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'prioridad': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'miembros.zona': {
            'Meta': {'object_name': 'Zona'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['academia']