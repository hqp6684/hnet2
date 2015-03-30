from django.db import models
from users.models import Patient, Doctor, Nurse, UserProfile
from django.contrib.auth.models import User
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField, PhoneNumberField
from django.core.urlresolvers import reverse
#to track model 
from simple_history.models import HistoricalRecords

#to exclude custom fields when migrate with sould
#from south.modelsinspector import add_introspection_rules
#add_introspection_rules([], ["^localflavor\.us\.models"])


# Create your models here.


class MedicalInformation(models.Model):
	history = HistoricalRecords()
	patient = models.OneToOneField(Patient, primary_key=True, verbose_name='related Patient')
	primary_doc = models.ForeignKey(Doctor, verbose_name='Primary Doctor', null=True)
	initialized = models.BooleanField(default=False)
	legal_name = models.CharField(max_length=100, blank=True)
	legal_name1 = models.CharField(max_length=100, blank=True)

	dOB = models.DateField(null=True)


	class Meta:
		permissions = (
			("init_medinfo", "can initialize med-info"),
			("read_medinfo", "can view med-info"),
		)

	@classmethod
	def create(info, patient):
		new_info = info(patient=patient)
		return new_info
	def __str__(self):
		return self.patient.patient.username

class ChronicMedicalProblems(models.Model):
	#history = HistoricalRecords()
	medinfo = models.OneToOneField(MedicalInformation, verbose_name="Med-info")
	high_blood = models.BooleanField(default=False, verbose_name="High Blood Pressure")
	heart = models.BooleanField(default=False, verbose_name="Heart Disease")
	diabete = models.BooleanField(default=False, verbose_name="Diabetes")
	stroke = models.BooleanField(default=False, verbose_name="Stroke")
	cancer = models.BooleanField(default=False, verbose_name="Cancer")
	thyroid = models.BooleanField(default=False, verbose_name="Thyroid")
	asthma = models.BooleanField(default=False, verbose_name="Asthma")
	other = models.CharField(max_length=200, blank=True, verbose_name="Others")


class EmergencyContact(models.Model):
	#history = HistoricalRecords()
	patient = models.OneToOneField(Patient, primary_key=True)
	name = models.CharField(max_length=100, blank=True, verbose_name="Emergency Contact Name")
	phone = PhoneNumberField(blank=True, verbose_name="Phone")
	relationship = models.CharField(max_length=20, blank=True, verbose_name="relationship to patient")

class InsuranceInformation(models.Model):
	#history = HistoricalRecords()
	patient = models.OneToOneField(Patient, primary_key=True, verbose_name='Related Patient')
	policy_holder = models.CharField(max_length=100, verbose_name="Policy Holder", blank=True)
	carrier = models.CharField(max_length=100, verbose_name="Insurance Carrier", blank=True)
	policy_number = models.CharField(max_length=10, verbose_name="Policy Number", blank=True)





