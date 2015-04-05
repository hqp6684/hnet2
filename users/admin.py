from django.contrib import admin
from users.models import UserProfile, Patient, Employee, Doctor, Receptionist, Nurse
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Patient, SimpleHistoryAdmin)
admin.site.register(Employee)
admin.site.register(Doctor)
admin.site.register(Nurse)

admin.site.register(Receptionist)