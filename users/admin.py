from django.contrib import admin
from .models import UserProfile, Patient, Employee, Doctor
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Patient)
admin.site.register(Employee)
admin.site.register(Doctor)