# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MedicalInformation'
        db.create_table('medicalinfo_medicalinformation', (
            ('patient', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Patient'], unique=True, primary_key=True)),
            ('primary_doc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Doctor'], null=True)),
            ('initialized', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('legal_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('dOB', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('medicalinfo', ['MedicalInformation'])

        # Adding model 'ChronicMedicalProblems'
        db.create_table('medicalinfo_chronicmedicalproblems', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('medinfo', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['medicalinfo.MedicalInformation'], unique=True)),
            ('high_blood', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('heart', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('diabete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('stroke', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cancer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thyroid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('asthma', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('other', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('medicalinfo', ['ChronicMedicalProblems'])

        # Adding model 'EmergencyContact'
        db.create_table('medicalinfo_emergencycontact', (
            ('patient', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Patient'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('medicalinfo', ['EmergencyContact'])

        # Adding model 'InsuranceInformation'
        db.create_table('medicalinfo_insuranceinformation', (
            ('patient', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Patient'], unique=True, primary_key=True)),
            ('policy_holder', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('carrier', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('policy_number', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal('medicalinfo', ['InsuranceInformation'])


    def backwards(self, orm):
        # Deleting model 'MedicalInformation'
        db.delete_table('medicalinfo_medicalinformation')

        # Deleting model 'ChronicMedicalProblems'
        db.delete_table('medicalinfo_chronicmedicalproblems')

        # Deleting model 'EmergencyContact'
        db.delete_table('medicalinfo_emergencycontact')

        # Deleting model 'InsuranceInformation'
        db.delete_table('medicalinfo_insuranceinformation')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
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
            'medinfo': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['medicalinfo.MedicalInformation']", 'unique': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'stroke': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thyroid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'medicalinfo.emergencycontact': {
            'Meta': {'object_name': 'EmergencyContact'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['users.Patient']", 'unique': 'True', 'primary_key': 'True'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'medicalinfo.insuranceinformation': {
            'Meta': {'object_name': 'InsuranceInformation'},
            'carrier': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['users.Patient']", 'unique': 'True', 'primary_key': 'True'}),
            'policy_holder': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'policy_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'medicalinfo.medicalinformation': {
            'Meta': {'object_name': 'MedicalInformation'},
            'dOB': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'initialized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['users.Patient']", 'unique': 'True', 'primary_key': 'True'}),
            'primary_doc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Doctor']", 'null': 'True'})
        },
        'users.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'doctor': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['users.Employee']", 'unique': 'True', 'primary_key': 'True'}),
            'max_patients': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'})
        },
        'users.employee': {
            'Meta': {'object_name': 'Employee'},
            'employee': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'employee_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'users.patient': {
            'Meta': {'object_name': 'Patient'},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'primary_doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Doctor']", 'null': 'True'})
        }
    }

    complete_apps = ['medicalinfo']