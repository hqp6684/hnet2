# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MedicalInformation.legal_name1'
        db.add_column('medicalinfo_medicalinformation', 'legal_name1',
                      self.gf('django.db.models.fields.CharField')(max_length=100, blank=True, default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MedicalInformation.legal_name1'
        db.delete_column('medicalinfo_medicalinformation', 'legal_name1')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'medicalinfo.chronicmedicalproblems': {
            'Meta': {'object_name': 'ChronicMedicalProblems'},
            'asthma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cancer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'diabete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'high_blood': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medinfo': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['medicalinfo.MedicalInformation']"}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'stroke': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thyroid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'medicalinfo.emergencycontact': {
            'Meta': {'object_name': 'EmergencyContact'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['users.Patient']"}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'medicalinfo.insuranceinformation': {
            'Meta': {'object_name': 'InsuranceInformation'},
            'carrier': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['users.Patient']"}),
            'policy_holder': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'policy_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'medicalinfo.medicalinformation': {
            'Meta': {'object_name': 'MedicalInformation'},
            'dOB': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'initialized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'legal_name1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['users.Patient']"}),
            'primary_doc': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['users.Doctor']"})
        },
        'users.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'doctor': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['users.Employee']"}),
            'max_patients': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'})
        },
        'users.employee': {
            'Meta': {'object_name': 'Employee'},
            'employee': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['auth.User']"}),
            'employee_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'users.patient': {
            'Meta': {'object_name': 'Patient'},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['auth.User']"}),
            'primary_doctor': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['users.Doctor']"})
        }
    }

    complete_apps = ['medicalinfo']