from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField, PhoneNumberField
from django.core.urlresolvers import reverse
# Create your models here.

#to exclude custom fields when migrate with sould
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^localflavor\.us\.models"])

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	#use ref_id to hind user_id
	ref_id = models.CharField(max_length=120, default='abc', unique=True)
	fName = models.CharField(max_length=40, verbose_name ="First Name")
	lName = models.CharField(max_length=40, verbose_name ="Last Name", )
	mName = models.CharField(max_length=40, verbose_name ="Middle Name", )
	dOB = models.DateField()
	sSN = USSocialSecurityNumberField(verbose_name ="SSN", unique=True, )
	phoneNumber = PhoneNumberField(null=True, verbose_name ="Phone")
	streetAddress = models.CharField(max_length=100, verbose_name ="Street")
	city = models.CharField(max_length=30, verbose_name ="City")
	state = USStateField(verbose_name ="State")
	zipcode = USZipCodeField(verbose_name ="Zipcode")
	email = models.EmailField(max_length=75, verbose_name ="Email", unique=True)
	dateJoin = models.DateField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)


	def __str__(self):
		return self.user.username


	'''return url for an object'''
	def get_absolute_url(self):
		#return "/users/%i/" % self.user.id
		return reverse('userprofile-detail', kwargs={'ref_id':self.ref_id})
	def get_absolute_url_update(self):
		return reverse('userprofile-update', kwargs={'ref_id':self.ref_id})




class Patient(models.Model):

	patient = models.OneToOneField(User,primary_key=True)
	is_active = models.BooleanField(default=False)

	'''
	doctor = models.ManyToManyField(Doctor)
	@classmethod
	def create(p, username):
		patient = p(user=usearname)
		return patient
'''
	def __str__(self):
		return self.patient.username


class Employee(models.Model):
	employee = models.OneToOneField(User, primary_key=True, verbose_name="Employee username")
	
	EMPLOYEE_CHOICES = (
		('D', 'Doctor'),
		('N', 'Nurse'),
		('R', 'Receptionist'),
		)
	#to translate, use get_employee_type_display
	employee_type = models.CharField(max_length=1, choices=EMPLOYEE_CHOICES)
	

	def __str__(self):
		return self.employee_type + " " + self.employee.username
	def _employee_info(self):
		info = self.employee_type + " " + self.employee.username
		return info

class Doctor(models.Model):
	doctor = models.OneToOneField(Employee, primary_key=True)

	def __str__(self):
		return self.doctor._employee_info()
	@classmethod
	def create(doc, employee):
		doctor = doc(doctor=employee)
		return doctor

class Nurse(models.Model):
	nurse = models.OneToOneField(Employee, primary_key=True)

	@classmethod
	def create(nur, employee):
		nurse = nur(nurse=employee)
		return nurse

	def __str__(self):
		return self.nurse._employee_info()











