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
    error_css_class = 'form-group has-error'

    class Meta:
        model = MedicalInformation
        exclude = ['patient', 'initialized']
        widgets = {
            'fName' : forms.TextInput(attrs={'class':'form-control '}),
            'lName' : forms.TextInput(attrs={'class':'form-control'}),
            'mName' : forms.TextInput(attrs={'class':'form-control'}),
        }
class CaseInitForm(forms.ModelForm):

    class Meta:
        model = Case
        exclude = ['medinfo','status','diagnosis','test_result','last_action']
        widgets = {
            'problem' : forms.Textarea(attrs={'class':'form-control', 'rows':6}),
        }

class CaseForm(forms.ModelForm):
    error_css_class = 'form-group has-error'

    class Meta:
        model = Case
        exclude = ['medinfo', 'last_action']
        widgets = {
            'status' : forms.Select(attrs={'class':'form-control '}),
            'diagnosis' : forms.TextInput(attrs={'class':'form-control '}),
            'test_result' : forms.TextInput(attrs={'class':'form-control '}),
            'problem' : forms.Textarea(attrs={'class':'form-control', 'rows':6}),
        }

class PrescriptionForm(forms.ModelForm):

    class Meta: 
        model = Prescription
        exclude = ['case']


class MedinfoViewForm(forms.ModelForm):

    class Meta:
        model = MedicalInformation

        

class EmergencyContactForm(forms.ModelForm):
    error_css_class = 'form-group has-error'

    class Meta:
        model = EmergencyContact
        exclude = ['patient']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control '}),
            'phone' : forms.TextInput(attrs={'class':'form-control'}),
            'relationship' : forms.TextInput(attrs={'class':'form-control'}),
        }


class InsuranceInformationForm(forms.ModelForm):
    error_css_class = 'form-group has-error'

    class Meta:
        model = InsuranceInformation
        exclude = ['patient']
        widgets = {
            'policy_holder' : forms.TextInput(attrs={'class':'form-control '}),
            'carrier' : forms.Select(attrs={'class':'form-control'}),
            'policy_number' : forms.TextInput(attrs={'class':'form-control'}),
        }

class AllergenForm(forms.ModelForm):
    error_css_class = 'form-group has-error'

    class Meta:
        model = Allergen
        exclude = ['medinfo']
        widgets = {
            'food_allegies' : forms.TextInput(attrs={'class':'form-control '}),
            'drug_allegies' : forms.Select(attrs={'class':'form-control'}),
            'environmental_allegies' : forms.TextInput(attrs={'class':'form-control'}),
        }







