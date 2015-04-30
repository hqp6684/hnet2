from django.db import models
from users.models import Patient, Doctor, Nurse, UserProfile
from django.contrib.auth.models import User
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField, PhoneNumberField
from django.core.urlresolvers import reverse
#to track model 
from simple_history.models import HistoricalRecords


#===========================================================================
#===========================================================================
#Each patient will have one medinfo instance, this contains 
#basic medinfo such as history, allergies, emergency contact and 
#insurance information
#===========================================================================
#===========================================================================

class MedicalInformation(models.Model):
	history = HistoricalRecords()
	patient = models.OneToOneField(Patient, primary_key=True, verbose_name='Patient')
	initialized = models.BooleanField(default=False)
	fName = models.CharField(max_length=40, verbose_name ="First Name")
	lName = models.CharField(max_length=40, verbose_name ="Last Name",)
	mName = models.CharField(max_length=40, verbose_name ="Middle Name", blank=True )

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
		return self.patient.patient.username + "medinfo"

#===========================================================================
#===========================================================================
#Link to medinfo
#
#===========================================================================
#===========================================================================

class ChronicMedicalProblems(models.Model):
	history = HistoricalRecords()
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

#===========================================================================
#===========================================================================
#link to medinfo
#
#===========================================================================
#===========================================================================

class Allergen(models.Model):
	history = HistoricalRecords()
	medinfo = models.OneToOneField(MedicalInformation, verbose_name="Med-info", primary_key=True)
	food = models.BooleanField(default=False, verbose_name="Food Allergic")
	food_allegies = models.CharField(max_length=200, blank=True, verbose_name="Food")
	drug = models.BooleanField(default=False, verbose_name="Drug Allergic")
	drug_allegies = models.CharField(max_length=200, blank=True, verbose_name="Drugs")
	environmental = models.BooleanField(default=False, verbose_name="Environmental Allergic")
	environmental_allegies = models.CharField(max_length=200, blank=True, verbose_name="Environment")

	def __str__(self):
		return self.medinfo.patient.patient.username

#===========================================================================
#===========================================================================
#Link to medinfo
#
#===========================================================================
#===========================================================================

class EmergencyContact(models.Model):
	history = HistoricalRecords()
	patient = models.OneToOneField(Patient, primary_key=True)
	name = models.CharField(max_length=100, blank=True, verbose_name="Emergency Contact Name")
	phone = PhoneNumberField(blank=True, verbose_name="Phone")
	relationship = models.CharField(max_length=20, blank=True, verbose_name="relationship to patient")

	def __str__(self):
		return self.patient.patient.username

#===========================================================================
#===========================================================================
#Link to med info
#
#===========================================================================
#===========================================================================

class InsuranceInformation(models.Model):
	INSURANCE_CHOICES = (
        ('B', 'Blue Choice Options'),
        ('U', 'United Healthcare'),
        ('M', 'Medicaid'),
        ('N', 'None'),
        )

	history = HistoricalRecords()
	patient = models.OneToOneField(Patient, primary_key=True, verbose_name='Related Patient')
	policy_holder = models.CharField(max_length=100, verbose_name="Policy Holder", blank=True)
	carrier = models.CharField(max_length=1, verbose_name="Insurance Carrier", choices=INSURANCE_CHOICES, default='N')
	policy_number = models.CharField(max_length=10, verbose_name="Policy Number", blank=True)

	def __str__(self):
		return self.patient.patient.username

#===========================================================================
#===========================================================================
#
#When a patient have a problem, a case will be created and will be used by doctor to 
#diagnose, update test result, and prescription
#
#===========================================================================
#===========================================================================

class Case(models.Model):
	CASE_STATUS_CHOICES = (
        ('A', 'Active'),
        ('C', 'Closed'),
        ('N', 'New'),
        )
	LAST_ACTION_CHOIES = (
		('N', 'Created'),
		('D', 'Updated'),
		('P', 'New Prescription Updated'),
		)

	history = HistoricalRecords()
	medinfo = models.ForeignKey(MedicalInformation, verbose_name="Med-info")
	status = models.CharField(max_length=1, choices=CASE_STATUS_CHOICES, verbose_name='Case Status', default='N')
	problem = models.CharField(max_length=200, verbose_name='Problem/Concern')
	diagnosis = models.CharField(max_length=200, verbose_name='Diagnosis', default='None')
	test_result = models.CharField(max_length=200, verbose_name='Test Result', default='None')
	last_action = models.CharField(max_length=1, choices=LAST_ACTION_CHOIES, verbose_name='Last action', default='N')
	created = models.DateField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.problem


#===========================================================================
#===========================================================================
#Each case will have 0-* presciptions 
#
#===========================================================================
#===========================================================================

class Prescription(models.Model):
	history = HistoricalRecords()
	case = models.ForeignKey(Case, verbose_name="Related Case")
	drug = models.CharField(max_length=200, verbose_name="Drug")
	instruction = models. CharField(max_length=200, verbose_name="Instruction")
	refill = models.PositiveSmallIntegerField(default=0, verbose_name="Refill")
	created = models.DateField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.case + " " + self.drug



