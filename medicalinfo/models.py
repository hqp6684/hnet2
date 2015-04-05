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
	#history = HistoricalRecords()
	patient = models.OneToOneField(Patient, primary_key=True, verbose_name='Patient')
	#primary_doc = models.ForeignKey(Doctor, verbose_name='Primary Doctor', null=True)

	initialized = models.BooleanField(default=False)
	fName = models.CharField(max_length=40, verbose_name ="First Name")
	lName = models.CharField(max_length=40, verbose_name ="Last Name",)
	mName = models.CharField(max_length=40, verbose_name ="Middle Name", blank=True )

	problem = models.CharField(max_length=200, verbose_name="Your concerns/problems")
	#dOB = models.DateField(null=True)
	#current_problem = models.CharField(max_length=200, blank=True)



	class Meta:
		permissions = (
			("init_medinfo", "can initialize med-info"),
			("read_medinfo", "can view med-info"),
			("init_case", "can init diagnosis"),
		)

	@classmethod
	def create(info, patient):
		new_info = info(patient=patient)
		return new_info
	def __str__(self):
		return self.patient.patient.username

class ChronicMedicalProblems(models.Model):
	#history = HistoricalRecords()
	medinfo = models.OneToOneField(MedicalInformation, verbose_name="Med-info", primary_key=True)
	high_blood = models.BooleanField(default=False, verbose_name="High Blood Pressure")
	heart = models.BooleanField(default=False, verbose_name="Heart Disease")
	diabete = models.BooleanField(default=False, verbose_name="Diabetes")
	stroke = models.BooleanField(default=False, verbose_name="Stroke")
	cancer = models.BooleanField(default=False, verbose_name="Cancer")
	thyroid = models.BooleanField(default=False, verbose_name="Thyroid")
	asthma = models.BooleanField(default=False, verbose_name="Asthma")
	other = models.CharField(max_length=200, blank=True, verbose_name="Others")

	def __str__(self):
		return self.medinfo.patient.patient.username

class Allergen(models.Model):
	medinfo = models.OneToOneField(MedicalInformation, verbose_name="Med-info", primary_key=True)
	food = models.BooleanField(default=False, verbose_name="Food Allergic")
	food_allegies = models.CharField(max_length=200, blank=True, verbose_name="Food")
	drug = models.BooleanField(default=False, verbose_name="Drug Allergic")
	drug_allegies = models.CharField(max_length=200, blank=True, verbose_name="Drugs")
	environmental = models.BooleanField(default=False, verbose_name="Environmental Allergic")
	environmental_allegies = models.CharField(max_length=200, blank=True, verbose_name="Environment")

	def __str__(self):
		return self.medinfo.patient.patient.username


class EmergencyContact(models.Model):
	#history = HistoricalRecords
	patient = models.OneToOneField(Patient, primary_key=True)
	name = models.CharField(max_length=100, blank=True, verbose_name="Emergency Contact Name")
	phone = PhoneNumberField(blank=True, verbose_name="Phone")
	relationship = models.CharField(max_length=20, blank=True, verbose_name="relationship to patient")

	def __str__(self):
		return self.patient.patient.username


class InsuranceInformation(models.Model):
	#history = HistoricalRecords()
	patient = models.OneToOneField(Patient, primary_key=True, verbose_name='Related Patient')
	policy_holder = models.CharField(max_length=100, verbose_name="Policy Holder", blank=True)
	carrier = models.CharField(max_length=100, verbose_name="Insurance Carrier", blank=True)
	policy_number = models.CharField(max_length=10, verbose_name="Policy Number", blank=True)

	def __str__(self):
		return self.patient.patient.username

class Case(models.Model):
	#history = HistoricalRecords()
	patient = models.ForeignKey(Patient, verbose_name='Related Patient')
	problem = models.CharField(max_length=200, verbose_name='Reason')
	diagnosis = models.CharField(max_length=200, verbose_name='Diagnosis')
	test_result = models.CharField(max_length=200, verbose_name='Test Result')
	check_in = models.DateField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)



