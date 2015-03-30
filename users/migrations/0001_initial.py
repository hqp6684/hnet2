# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('users_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['auth.User'])),
            ('ref_id', self.gf('django.db.models.fields.CharField')(max_length=120, unique=True, default='abc')),
            ('fName', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('lName', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('mName', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('dOB', self.gf('django.db.models.fields.DateField')()),
            ('sSN', self.gf('localflavor.us.models.USSocialSecurityNumberField')(max_length=11, unique=True)),
            ('phoneNumber', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, null=True)),
            ('streetAddress', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('state', self.gf('localflavor.us.models.USStateField')(max_length=2)),
            ('zipcode', self.gf('localflavor.us.models.USZipCodeField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, unique=True)),
            ('dateJoin', self.gf('django.db.models.fields.DateField')(blank=True, auto_now_add=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('users', ['UserProfile'])

        # Adding model 'Employee'
        db.create_table('users_employee', (
            ('employee', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['auth.User'])),
            ('employee_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('users', ['Employee'])

        # Adding model 'Doctor'
        db.create_table('users_doctor', (
            ('doctor', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['users.Employee'])),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('max_patients', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
        ))
        db.send_create_signal('users', ['Doctor'])

        # Adding model 'Nurse'
        db.create_table('users_nurse', (
            ('nurse', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['users.Employee'])),
        ))
        db.send_create_signal('users', ['Nurse'])

        # Adding model 'Receptionist'
        db.create_table('users_receptionist', (
            ('receptionist', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['users.Employee'])),
        ))
        db.send_create_signal('users', ['Receptionist'])

        # Adding model 'Patient'
        db.create_table('users_patient', (
            ('patient', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['auth.User'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('primary_doctor', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['users.Doctor'])),
        ))
        db.send_create_signal('users', ['Patient'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('users_userprofile')

        # Deleting model 'Employee'
        db.delete_table('users_employee')

        # Deleting model 'Doctor'
        db.delete_table('users_doctor')

        # Deleting model 'Nurse'
        db.delete_table('users_nurse')

        # Deleting model 'Receptionist'
        db.delete_table('users_receptionist')

        # Deleting model 'Patient'
        db.delete_table('users_patient')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'doctor': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['users.Employee']"}),
            'max_patients': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'})
        },
        'users.employee': {
            'Meta': {'object_name': 'Employee'},
            'employee': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"}),
            'employee_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'users.nurse': {
            'Meta': {'object_name': 'Nurse'},
            'nurse': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['users.Employee']"})
        },
        'users.patient': {
            'Meta': {'object_name': 'Patient'},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'patient': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"}),
            'primary_doctor': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['users.Doctor']"})
        },
        'users.receptionist': {
            'Meta': {'object_name': 'Receptionist'},
            'receptionist': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['users.Employee']"})
        },
        'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'dOB': ('django.db.models.fields.DateField', [], {}),
            'dateJoin': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True'}),
            'fName': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'mName': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'phoneNumber': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True'}),
            'ref_id': ('django.db.models.fields.CharField', [], {'max_length': '120', 'unique': 'True', 'default': "'abc'"}),
            'sSN': ('localflavor.us.models.USSocialSecurityNumberField', [], {'max_length': '11', 'unique': 'True'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'streetAddress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"}),
            'zipcode': ('localflavor.us.models.USZipCodeField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['users']