from django.contrib import admin
from medicalinfo.models import MedicalInformation
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(MedicalInformation, SimpleHistoryAdmin)