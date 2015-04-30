from django.contrib import admin
from users.models import UserProfile, Patient, Employee, Doctor, Receptionist, Nurse
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

admin.site.register(UserProfile,SimpleHistoryAdmin)
admin.site.register(Patient, SimpleHistoryAdmin)
admin.site.register(Employee,SimpleHistoryAdmin)
admin.site.register(Doctor,SimpleHistoryAdmin)
admin.site.register(Nurse,SimpleHistoryAdmin)
admin.site.register(Receptionist,SimpleHistoryAdmin)