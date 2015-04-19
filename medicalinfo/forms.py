from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile, Patient, Employee
from django.forms.models import model_to_dict, fields_for_model
from django.utils.translation import ugettext, ugettext_lazy as _


from localflavor.us.forms import USSocialSecurityNumberField, USPhoneNumberField

from medicalinfo.models import (MedicalInformation, ChronicMedicalProblems, 
    EmergencyContact, InsuranceInformation, Allergen, Case, Prescription,
)


class ChronicMedicalProblemsForm(forms.ModelForm):
    class Meta:
        model = ChronicMedicalProblems
        exclude = ['medinfo']

class MedinfoInitForm(forms.ModelForm):
    class Meta:
        model = MedicalInformation
        exclude = ['patient', 'primary_doc', 'initialized']

class CaseInitForm(forms.ModelForm):

    class Meta:
        model = Case
        exclude = ['medinfo','status','diagnosis','test_result','last_action']
  
class CaseForm(forms.ModelForm):

    class Meta:
        model = Case
        exclude = ['medinfo', 'last_action']

class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        exclude = ['case']

'''
    def __init__(self, *args, **kwargs):
        my_medinfo = kwargs.pop('medinfo')
        super(CaseInitForm, self).__init__(*args, **kwargs)
        self.fields['medinfo'] = my_medinfo
'''

class MedinfoViewForm(forms.ModelForm):

    class Meta:
        model = MedicalInformation

        

class EmergencyContactForm(forms.ModelForm):

    class Meta:
        model = EmergencyContact
        exclude = ['patient']


class InsuranceInformationForm(forms.ModelForm):

    class Meta:
        model = InsuranceInformation
        exclude = ['patient']

class AllergenForm(forms.ModelForm):

    class Meta:
        model = Allergen
        exclude = ['medinfo']







