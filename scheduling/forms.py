from django.forms import ModelForm, widgets
from django import forms
from scheduling.models import Appointment
#from bootstrap3_datetime.widgets import DateTimePicker
from users.models import is_patient, is_nurse, is_employee, is_doctor, Patient, Doctor


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
