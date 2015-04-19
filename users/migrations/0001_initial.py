# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'users_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('ref_id', self.gf('django.db.models.fields.CharField')(default='abc', unique=True, max_length=120)),
            ('fName', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('lName', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('mName', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('dOB', self.gf('django.db.models.fields.DateField')()),
            ('sSN', self.gf('localflavor.us.models.USSocialSecurityNumberField')(unique=True, max_length=11)),
            ('phoneNumber', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, null=True)),
            ('streetAddress', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('state', self.gf('localflavor.us.models.USStateField')(max_length=2)),
            ('zipcode', self.gf('localflavor.us.models.USZipCodeField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('dateJoin', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['UserProfile'])

        # Adding model 'Employee'
        db.create_table(u'users_employee', (
            ('employee', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('employee_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'users', ['Employee'])

        # Adding model 'Doctor'
        db.create_table(u'users_doctor', (
            ('doctor', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Employee'], unique=True, primary_key=True)),
            ('specialty', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=100)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('max_patients', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
            ('current_patient_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'users', ['Doctor'])

        # Adding model 'Nurse'
        db.create_table(u'users_nurse', (
            ('nurse', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Employee'], unique=True, primary_key=True)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('max_patients', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=10)),
            ('current_patient_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'users', ['Nurse'])

        # Adding model 'Receptionist'
        db.create_table(u'users_receptionist', (
            ('receptionist', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.Employee'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'users', ['Receptionist'])

        # Adding model 'Patient'
        db.create_table(u'users_patient', (
            ('patient', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('primary_doctor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_doctor', null=True, to=orm['users.Doctor'])),
            ('primary_nurse', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_nurse', null=True, to=orm['users.Nurse'])),
        ))
        db.send_create_signal(u'users', ['Patient'])

        # Adding M2M table for field doctors on 'Patient'
        m2m_table_name = db.shorten_name(u'users_patient_doctors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patient', models.ForeignKey(orm[u'users.patient'], null=False)),
            ('doctor', models.ForeignKey(orm[u'users.doctor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patient_id', 'doctor_id'])

        # Adding M2M table for field nurses on 'Patient'
        m2m_table_name = db.shorten_name(u'users_patient_nurses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patient', models.ForeignKey(orm[u'users.patient'], null=False)),
            ('nurse', models.ForeignKey(orm[u'users.nurse'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patient_id', 'nurse_id'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'users_userprofile')

        # Deleting model 'Employee'
        db.delete_table(u'users_employee')

        # Deleting model 'Doctor'
        db.delete_table(u'users_doctor')

        # Deleting model 'Nurse'
        db.delete_table(u'users_nurse')

        # Deleting model 'Receptionist'
        db.delete_table(u'users_receptionist')

        # Deleting model 'Patient'
        db.delete_table(u'users_patient')

        # Removing M2M table for field doctors on 'Patient'
        db.delete_table(db.shorten_name(u'users_patient_doctors'))

        # Removing M2M table for field nurses on 'Patient'
        db.delete_table(db.shorten_name(u'users_patient_nurses'))


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
        },
        u'users.receptionist': {
            'Meta': {'object_name': 'Receptionist'},
            'receptionist': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['users.Employee']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'dOB': ('django.db.models.fields.DateField', [], {}),
            'dateJoin': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'fName': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'lName': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'mName': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'phoneNumber': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True'}),
            'ref_id': ('django.db.models.fields.CharField', [], {'default': "'abc'", 'unique': 'True', 'max_length': '120'}),
            'sSN': ('localflavor.us.models.USSocialSecurityNumberField', [], {'unique': 'True', 'max_length': '11'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'streetAddress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'zipcode': ('localflavor.us.models.USZipCodeField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['users']