# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Prescription'
        db.create_table(u'medicalinfo_prescription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('case', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medicalinfo.Case'])),
            ('drug', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intruction', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('refill', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'medicalinfo', ['Prescription'])


    def backwards(self, orm):
        # Deleting model 'Prescription'
        db.delete_table(u'medicalinfo_prescription')


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
        u'medicalinfo.allergen': {
            'Meta': {'object_name': 'Allergen'},
            'drug': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'drug_allegies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'environmental': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'environmental_allegies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'food': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'food_allegies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'medinfo': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['medicalinfo.MedicalInformation']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'medicalinfo.case': {
            'Meta': {'object_name': 'Case'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diagnosis': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medinfo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medicalinfo.MedicalInformation']"}),
            'problem': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'test_result': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'medicalinfo.chronicmedicalproblems': {
            'Meta': {'object_name': 'ChronicMedicalProblems'},
            'asthma': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cancer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'diabete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'high_blood': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'medinfo': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['medicalinfo.MedicalInformation']", 'unique': 'True', 'primary_key': 'True'}),
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
            'fName': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'initialized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'mName': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.Patient']", 'unique': 'True', 'primary_key': 'True'}),
            'problem': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'medicalinfo.prescription': {
            'Meta': {'object_name': 'Prescription'},
            'case': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medicalinfo.Case']"}),
            'drug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intruction': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'refill': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'users.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_patient_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'doctor': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.Employee']", 'unique': 'True', 'primary_key': 'True'}),
            'max_patients': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'}),
            'specialty': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '100'})
        },
        u'users.employee': {
            'Meta': {'object_name': 'Employee'},
            'employee': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'employee_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'users.nurse': {
            'Meta': {'object_name': 'Nurse'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_patient_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'max_patients': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'}),
            'nurse': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.Employee']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'users.patient': {
            'Meta': {'object_name': 'Patient'},
            'doctors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Doctor']", 'null': 'True', 'symmetrical': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nurses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.Nurse']", 'null': 'True', 'symmetrical': 'False'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'primary_doctor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_doctor'", 'null': 'True', 'to': u"orm['users.Doctor']"}),
            'primary_nurse': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_nurse'", 'null': 'True', 'to': u"orm['users.Nurse']"})
        }
    }

    complete_apps = ['medicalinfo']