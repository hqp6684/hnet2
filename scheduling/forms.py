from django.forms import ModelForm, widgets
from django import forms
from scheduling.models import Appointment
#from bootstrap3_datetime.widgets import DateTimePicker
from users.models import is_patient, is_nurse, is_employee, is_doctor, Patient, Doctor

from datetime import datetime
from django.utils import timezone

class AppointmentForm(ModelForm):

    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form_datetime form-control'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form_datetime form-control'}))
    class Meta: # model must be in the Meta class
        model = Appointment
        #exclude =["start_time", "end_time"] 
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.TextInput(attrs={'class':'form-control'}),
            'patient': forms.Select(attrs={'class':'form-control'}),
            'doctor': forms.Select(attrs={'class':'form-control'}),
            'location': forms.Select(attrs={'class':'form-control'}),

        }

    def clean_start_time(self):
        start = self.cleaned_data['start_time']
        if start < timezone.now() :
            raise forms.ValidationError('Invalid start time')
        return start
    def clean_end_time(self):
        start = self.cleaned_data['start_time']
        end = self.cleaned_data['end_time']
        if end <= start:
            raise forms.ValidationError('Invalid end time')
        return end


    def set_query_sets(self, user):
        if is_patient(user):
            self.fields["patient"].queryset = Patient.objects.filter(patient = user)
            self.fields["doctor"].queryset = user.patient.doctors

        elif is_employee(user):

            if is_doctor(user):
                self.fields["doctor"].queryset = Doctor.objects.filter(doctor = user)
                self.fields["patient"].queryset = user.employee.doctor.patient_set
                print("doctor")
            else:
                pass

        else:
            pass
