from django.db import models
from users.models import Patient, Doctor, Nurse, UserProfile

# Create your models here.

class MedicalInformation(models.Model):
	patient = models.OneToOneField(Patient, primary_key=True)
	primary_doc = models.ForeignKey(Doctor, verbose_name='Primary Doctor')
	problem = models.CharField(max_length=200, blank=True)
	
