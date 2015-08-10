# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ReunionDiscipulado.ofrenda'
        db.alter_column('grupos_reuniondiscipulado', 'ofrenda', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2))

        # Changing field 'ReunionGAR.ofrenda'
        db.alter_column('grupos_reuniongar', 'ofrenda', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2))

    def backwards(self, orm):

        # Changing field 'ReunionDiscipulado.ofrenda'
        db.alter_column('grupos_reuniondiscipulado', 'ofrenda', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'ReunionGAR.ofrenda'
        db.alter_column('grupos_reuniongar', 'ofrenda', self.gf('django.db.models.fields.PositiveIntegerField')())

    models = {
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
        'grupos.asistenciadiscipulado': {
            'Meta': {'object_name': 'AsistenciaDiscipulado'},
            'asistencia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miembro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Miembro']"}),
            'reunion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grupos.ReunionDiscipulado']"})
        },
        'grupos.asistenciamiembro': {
            'Meta': {'object_name': 'AsistenciaMiembro'},
            'asistencia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miembro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Miembro']"}),
            'reunion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grupos.ReunionGAR']"})
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
        'grupos.predica': {
            'Meta': {'object_name': 'Predica'},
            'descripcion': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miembro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['miembros.Miembro']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'grupos.red': {
            'Meta': {'object_name': 'Red'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'grupos.reuniondiscipulado': {
            'Meta': {'object_name': 'ReunionDiscipulado'},
            'asistentecia': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['miembros.Miembro']", 'through': "orm['grupos.AsistenciaDiscipulado']", 'symmetrical': 'False'}),
            'confirmacionEntregaOfrenda': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grupos.Grupo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'novedades': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'numeroLideresAsistentes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ofrenda': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'predica': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grupos.Predica']"})
        },
        'grupos.reuniongar': {
            'Meta': {'object_name': 'ReunionGAR'},
            'asistentecia': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['miembros.Miembro']", 'through': "orm['grupos.AsistenciaMiembro']", 'symmetrical': 'False'}),
            'confirmacionEntregaOfrenda': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['grupos.Grupo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'novedades': ('django.db.models.fields.TextField', [], {'default': "'nada'", 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'numeroLideresAsistentes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'numeroTotalAsistentes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'numeroVisitas': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ofrenda': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'predica': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'fecha': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 8, 10, 0, 0)'}),
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

    complete_apps = ['grupos']