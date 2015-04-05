from django.contrib import admin
from medicalinfo.models import MedicalInformation, ChronicMedicalProblems, EmergencyContact, InsuranceInformation
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(MedicalInformation, SimpleHistoryAdmin)
admin.site.register(ChronicMedicalProblems, SimpleHistoryAdmin)
admin.site.register(EmergencyContact, SimpleHistoryAdmin)
admin.site.register(InsuranceInformation, SimpleHistoryAdmin)