# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MedicalInformation'
        db.create_table(u'medicalinfo_medicalinformation', (
            ('patient', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Patient'], unique=True, primary_key=True)),
            ('initialized', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('legal_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('dOB', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'medicalinfo', ['MedicalInformation'])

        # Adding model 'ChronicMedicalProblems'
        db.create_table(u'medicalinfo_chronicmedicalproblems', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
        db.send_create_signal(u'medicalinfo', ['ChronicMedicalProblems'])

        # Adding model 'EmergencyContact'
        db.create_table(u'medicalinfo_emergencycontact', (
            ('patient', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Patient'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'medicalinfo', ['EmergencyContact'])

        # Adding model 'InsuranceInformation'
        db.create_table(u'medicalinfo_insuranceinformation', (
            ('patient', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Patient'], unique=True, primary_key=True)),
            ('policy_holder', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('carrier', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('policy_number', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal(u'medicalinfo', ['InsuranceInformation'])


    def backwards(self, orm):
        # Deleting model 'MedicalInformation'
        db.delete_table(u'medicalinfo_medicalinformation')

        # Deleting model 'ChronicMedicalProblems'
        db.delete_table(u'medicalinfo_chronicmedicalproblems')

        # Deleting model 'EmergencyContact'
        db.delete_table(u'medicalinfo_emergencycontact')

        # Deleting model 'InsuranceInformation'
        db.delete_table(u'medicalinfo_insuranceinformation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'medicalinfo.chronicmedicalproblems': {
            'Meta': {'object_name': 'ChronicMedicalProblems'},
            'asthma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cancer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'diabete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'high_blood': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medinfo': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['medicalinfo.MedicalInformation']", 'unique': 'True'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'stroke': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thyroid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'medicalinfo.emergencycontact': {
            'Meta': {'object_name': 'EmergencyContact'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.Patient']", 'unique': 'True', 'primary_key': 'True'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'medicalinfo.insuranceinformation': {
            'Meta': {'object_name': 'InsuranceInformation'},
            'carrier': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.Patient']", 'unique': 'True', 'primary_key': 'True'}),
            'policy_holder': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'policy_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        u'medicalinfo.medicalinformation': {
            'Meta': {'object_name': 'MedicalInformation'},
            'dOB': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'initialized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.Patient']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'users.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'doctor': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.Employee']", 'unique': 'True', 'primary_key': 'True'}),
            'max_patients': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'})
        },
        u'users.employee': {
            'Meta': {'object_name': 'Employee'},
            'employee': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'employee_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'users.patient': {
            'Meta': {'object_name': 'Patient'},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'primary_doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Doctor']", 'null': 'True'})
        }
    }

    complete_apps = ['medicalinfo']