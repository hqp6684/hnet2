from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField, PhoneNumberField
from django.core.urlresolvers import reverse
from simple_history.models import HistoricalRecords

# Create your models here.

#to exclude custom fields when migrate with sould
#from south.modelsinspector import add_introspection_rules
#add_introspection_rules([], ["^localflavor\.us\.models"])

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    #use ref_id to hind user_id
    ref_id = models.CharField(max_length=120, default='abc', unique=True)
    fName = models.CharField(max_length=40, verbose_name ="First Name")
    lName = models.CharField(max_length=40, verbose_name ="Last Name", )
    mName = models.CharField(max_length=40, verbose_name ="Middle Name", blank=True )
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

    '''return url for user object'''
    def get_absolute_url(self):
        #return "/users/%i/" % self.user.id
        return reverse('userprofile-detail', kwargs={'ref_id':self.ref_id})
    def get_absolute_url_update(self):
        return reverse('userprofile-update', kwargs={'ref_id':self.ref_id})
    def get_activate_url(self):
        return reverse('patient-activate', kwargs={'ref_id': self.ref_id})
    def get_discharge_url(self):
        return reverse('patient-discharge', kwargs={'ref_id': self.ref_id})
       

    #this is for med-info
    #get url to view user med-info
    def get_medinfo_url(self):
        return reverse('med-info-detail', kwargs={'ref_id': self.ref_id})
    #get url to init user med-info
    def get_medinfo_init_url(self):
        return reverse('med-info-init', kwargs={'ref_id': self.ref_id})





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
    doctor = models.OneToOneField(Employee, primary_key=True, verbose_name="Doctor")
    specialty = models.CharField(max_length=100, default="Unknown")
    available = models.BooleanField(default=True)
    max_patients = models.PositiveSmallIntegerField(default=10)
    current_patient_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.doctor._employee_info()

    @classmethod
    def create(doc, employee):
        doctor = doc(doctor=employee)
        return doctor


class Nurse(models.Model):
    nurse = models.OneToOneField(Employee, primary_key=True, verbose_name="Nurse")
    available = models.BooleanField(default=True)
    max_patients = models.PositiveSmallIntegerField(default=10)
    current_patient_count = models.PositiveSmallIntegerField(default=0)
  

    @classmethod
    def create(nur, employee):
        nurse = nur(nurse=employee)
        return nurse

    def __str__(self):
        return self.nurse._employee_info()


class Receptionist(models.Model):
    receptionist = models.OneToOneField(Employee, primary_key=True)

    @classmethod
    def create(rep, employee):
        receptionist = rep(receptionist=employee)
        return receptionist







class Patient(models.Model):
    #history = HistoricalRecords()
    patient = models.OneToOneField(User,primary_key=True)
    is_active = models.BooleanField(default=False)
    primary_doctor = models.ForeignKey(Doctor, verbose_name="Primary Doctor", related_name="primary_doctor", null=True)
    doctors = models.ManyToManyField(Doctor, verbose_name="Doctors", null=True)
    primary_nurse = models.ForeignKey(Nurse, verbose_name="Primary Nurse", related_name="primary_nurse", null=True)
    nurses = models.ManyToManyField(Nurse, verbose_name="Nurses", null=True)

    
    class Meta:
        permissions = (
            ("read_patient", "can view patient"),
            ("admit_patient", "can admit patient"),
            #to discharge, change is_active to false
            ("discharge_patient", "can discharge patient"),
        )
        
    def __str__(self):
        return self.patient.username




