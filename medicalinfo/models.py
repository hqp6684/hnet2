from django.db import models
from users.models import Patient, Doctor, Nurse, UserProfile


# Create your models here.
class MedicalInformation(models.Model):
	patient = models.OneToOneField(Patient, primary_key=True)
	primary_doc = models.ForeignKey(Doctor, verbose_name='Primary Doctor', null=True)
	problem = models.CharField(max_length=200, blank=True)
	initialized = models.BooleanField(default=False)

	class Meta:
		permissions = (
			("init_medinfo", "can initialize med-info"),
			("read_medinfo", "can view med-info"),
		)

	@classmethod
	def create(info, patient):
		new_info = info(patient=patient)
		return new_info


