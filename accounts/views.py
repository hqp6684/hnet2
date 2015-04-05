from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import UserProfile, Employee, Doctor, Nurse, Receptionist, Patient
from medicalinfo.models import MedicalInformation
from django.contrib import messages
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
import datetime

from .forms import (UserCreationForm, UserProfileForm, 
    NewPatientForm, AuthenticationForm, EmployeeCreationForm,
    PatientActivateForm, PatientDischargeForm,

)

from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth.models import User, Permission
from django.shortcuts import get_object_or_404



def account_message(request):
    context = {}
    template_name = 'accounts/account_message.html'
    return render(request, template_name, context)

#custom method to trace user_id by ref_id
def trace_user(ref_id):
    user = UserProfile.objects.get(ref_id=ref_id)
    return user.user
#method to give permissions to user
def gain_perms(user):
    #get permission instances
    read_medinfo = Permission.objects.get(codename='read_medinfo')
    init_medinfo = Permission.objects.get(codename='init_medinfo')
    edit_medinfo = Permission.objects.get(codename='change_medicalinformation')
    read_patient = Permission.objects.get(codename='read_patient')
    edit_patient = Permission.objects.get(codename='change_patient')
    admit_patient = Permission.objects.get(codename='admit_patient')
    discharge_patient = Permission.objects.get(codename='discharge_patient')

    try:
        if user.patient:
            user.user_permissions.add(read_medinfo)
            user.user_permissions.add(init_medinfo)
    except:
        if user.employee.employee_type == 'D':
            user.user_permissions.add(read_medinfo)
            user.user_permissions.add(init_medinfo)
            user.user_permissions.add(edit_medinfo)
            user.user_permissions.add(read_patient)
            user.user_permissions.add(edit_patient)
            user.user_permissions.add(admit_patient)
            user.user_permissions.add(discharge_patient)

        elif user.employee.employee_type == 'N':
            user.user_permissions.add(read_medinfo)
            user.user_permissions.add(init_medinfo)
            user.user_permissions.add(edit_medinfo)
            user.user_permissions.add(read_patient)
            user.user_permissions.add(edit_patient) 
            user.user_permissions.add(admit_patient)

        elif user.employee.employee_type == 'R':
            user.user_permissions.add(read_patient)
            user.user_permissions.add(admit_patient)





# Create your views here.
def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

''' create a random reference id for user'''
import uuid
def get_ref_id():
    ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
    try:
        id_exist = UserProfile.objects.get(ref_id=ref_id)
        get_ref_id()
    except:
        return ref_id

#patient registration method
def patient_register(request):

    form1 = UserCreationForm(prefix="u")
    form2 = UserProfileForm(prefix="p")
    form3 = NewPatientForm(prefix="n")

    if request.POST:
        #print request.POST
        form1 = UserCreationForm(request.POST, prefix="u")
        form2 = UserProfileForm(request.POST, prefix="p")


        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            profile = form2.save(commit=False)
            profile.user = user
            profile.ref_id = get_ref_id()
            profile.save()
            new_patient = form3.save(commit=False)
            new_patient.patient = user
            new_patient.save()
            #create new medinfo for this patient
            med_info = MedicalInformation.create(new_patient)
            med_info.save()
            messages.success(request, 'Thank you for joining us')
            #return to home 
            return redirect('/account/message')
        else:
            messages.error(request, 'Please correct all the fields with error')


    template_name = 'accounts/account_patient_form.html'
    context = {'form1': form1, 'form2':form2}
    return render(request, template_name, context)

def employee_register(request):
    form1 = UserCreationForm(prefix="u")
    form2 = UserProfileForm(prefix="p")
    form3 = EmployeeCreationForm(prefix="e")

    if request.POST:
        #print request.POST
        form1 = UserCreationForm(request.POST, prefix="u")
        form2 = UserProfileForm(request.POST, prefix="p")
        form3 = EmployeeCreationForm(request.POST, prefix="e")


        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            #user instance
            user = form1.save()
            #create user profile
            profile = form2.save(commit=False)
            profile.user = user
            #generate a new reference id for this user
            profile.ref_id = get_ref_id()
            #save to database
            profile.save()
            #create new employee instance
            new_employee = form3.save(commit=False)
            #set related user
            new_employee.employee = user

            #employee_type = new_employee.employee_type
            if new_employee.employee_type:
                #set medicalinfo permissions for user
                gain_perms(user)
                #create new doctor
                if new_employee.employee_type == 'D':
                    new_doc = Doctor.create(new_employee)
                    new_employee.save()
                    new_doc.save()
                    messages.success(request, 'A doctor has been registered')
                    #return to home 
                    return redirect('/account/message')
                elif new_employee.employee_type == 'N':
                    new_nurse = Nurse.create(new_employee)
                    new_employee.save()
                    new_nurse.save()
                    messages.success(request, 'A nurse has been registered')
                    #return to home 
                    return redirect('/account/message')

                elif new_employee.employee_type == 'R':
                    new_rep = Receptionist.create(new_employee)
                    new_employee.save()
                    new_rep.save()
                    messages.success(request, 'A Receptionist has been registered')
                    #return to home 
                    return redirect('/account/message')
                else:
                    messages.error(request, 'something wrong')
        else:
            messages.error(request, 'Please correct all the fields with error')


    template_name = 'accounts/account_employee_register_form.html'
    context = {'form1': form1, 'form2':form2, 'form3':form3}
    return render(request, template_name, context)


#==================================================================================
#==================================================================================
#           AUTHENTICATION
#           LOGIN-LOGOUT-USER PROFILE
#==================================================================================
#==================================================================================


def account_login(request, 
    template_name='accounts/account_login_form.html'):

    context = {}
    if request.user.is_authenticated():
        messages.info(request, 'You have already logged in')
        return redirect('/account/message')

    if request.method =='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)
            messages.success(request, 'You have successfully logged in')
            #check if patient is active and notify him/her to enroll
            try:
                if user.patient:
                    if not user.patient.is_active:
                        messages.info(request,'You are not registered as our patient yet. Please contact us for more information')
            except:
                pass
            return redirect('/account/message')
        else:
            messages.error(request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
    else:
        form = AuthenticationForm()
    context['form'] = form
    return render(request, template_name,context)


def account_logout(request,
           template_name='accounts/account_message.html'):

    auth_logout(request)
    context ={}
    messages.success(request, 'You have successfully logged out')
    return render(request, template_name, context)


@login_required
def userprofile_view(request, ref_id):
    template_name = 'accounts/account_profile_view_form.html'
    context = {}
    user_id = request.user.id
    profile = UserProfile.objects.get(pk=user_id)
    context['profile'] = profile
    return render(request, template_name, context)



@login_required
def userprofile_update(request, ref_id):
        template_name = 'accounts/account_profile_udpate_form.html'
        context = {}
        user_id = request.user.id
        profile = UserProfile.objects.get(pk=user_id)
        #initialize the form with exisiting profile(instance)
        form = UserProfileForm(request.POST or None, instance=profile)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully updated your profile information')
                return redirect('/account/%s' %ref_id)
            else:
                messages.error(request, 'Please correct the fields with error')

        context['form'] = form

        return render(request, template_name, context)





#==================================================================================
#==================================================================================
#           PATIENT-EMPLOYEE RELATIONSHIPS
#==================================================================================
#==================================================================================


#display all patients
@permission_required('users.read_patient', raise_exception=True)
def patient_list_view(request):
    template_name = 'accounts/account_patient_list.html'
    patients = Patient.objects.filter(is_active=True)
    context = {'patients':patients}

    return render(request, template_name, context)

#Display all inactive patients for admission 
@permission_required('users.read_patient', raise_exception=True)
def patient_inactive_list_view(request):
    template_name = 'accounts/account_patient_inactive_list.html'
    patients = Patient.objects.filter(is_active=False)
    context = {'patients':patients}
    return render(request, template_name, context)

#For doctor and nurse to see their patients
@permission_required('users.read_patient', raise_exception=True)
def my_patient_list_view(request):
    template_name = 'accounts/account_my_patient_list_view.html'
    #get user's patients
    context={}
    try:
        if request.user.employee.doctor:
            patients = request.user.employee.doctor.patient_set.filter(is_active=True)
    except:
        if request.user.employee.nurse:
            patients = request.user.employee.nurse.patient_set.filter(is_active=True)
    context = {'patients':patients}

    return render(request, template_name, context)

#For doctor and nurse to see all their patients (active/discharged patient)
@permission_required('users.read_patient', raise_exception=True)
def all_my_patient_list_view(request):
    template_name = 'accounts/account_all_my_patient_list_view.html'
    #get user's patients
    context={}
    try:
        if request.user.employee.doctor:
            patients = request.user.employee.doctor.patient_set.all()
    except:
        if request.user.employee.nurse:
            patients = request.user.employee.nurse.patient_set.all()
    context = {'patients':patients}

    return render(request, template_name, context)
    

#Patient admission
#Activate patient and set new permissions for patients
@permission_required('users.admit_patient', raise_exception=True)
#ref_id to get patient
def patient_activate(request, ref_id):
    template_name = 'accounts/account_patient_activate_form.html'
    #find patient by ref id
    p = trace_user(ref_id)
    #get patient instance
    patient = p.patient

    form = PatientActivateForm(request.POST or None, instance=patient)
    if request.POST:
        if form.is_valid():
            #update doctor
            #doctors = form.cleaned_data['doctors']
            form.save(commit=False)
            #update patient count for assigned doctor and nurses
            primary_doc = form.cleaned_data['primary_doctor']
            primary_doc.current_patient_count += 1
            if primary_doc.current_patient_count >= primary_doc.max_patients:
                primary_doc.available = False

            primary_doc.save()

            primary_nurse = form.cleaned_data['primary_nurse']
            primary_nurse.current_patient_count += 1
            if primary_nurse.current_patient_count >= primary_nurse.max_patients:
                primary_nurse.available = False
            

            primary_nurse.save()

            patient.doctors.add(primary_doc)
            patient.nurses.add(primary_nurse)

            form.save()



            messages.success(request,"You have admited patient %s" %p.username)
            #now give patient permission to init/read med-info
            gain_perms(p)
            return redirect('/account/message')
        else:
            messages.error(request, 'Please correct the fields with error')

    context = {'form':form, 'patient_username':p.username}
    return render(request, template_name, context)



#Patient charge
#Activate patient and set new permissions for patients
@permission_required('users.discharge_patient', raise_exception=True)
#ref_id to get patient
def patient_discharge(request, ref_id):
    template_name = 'accounts/account_patient_discharge_form.html'
    #find patient by ref id
    p = trace_user(ref_id)
    #get patient instance
    patient = p.patient

    form = PatientDischargeForm(request.POST or None, instance=patient)
    if request.POST:
        if form.is_valid():
            #update doctor
            #doctors = form.cleaned_data['doctors']
            form.save(commit=False)
            patient.is_active = False
            patient.save()
            #update patient count for assigned doctor and nurses
            doctors = patient.doctors.all()
            for doc in doctors:
                doc.current_patient_count -= 1
                if doc.current_patient_count < doc.max_patients:
                    doc.available = True

                doc.save()

            nurses = patient.nurses.all()
            for nurse in nurses:
                nurse.current_patient_count -= 1
                if nurse.current_patient_count > nurse.max_patients:
                    nurse.available = False

                nurse.save()



            messages.success(request,"You have discharged patient %s" %p.username)
            #now give patient permission to init/read med-info
            return redirect('/account/message')
        else:
            messages.error(request, 'Please correct the fields with error')

    context = {'form':form, 'patient_username':p.username}
    return render(request, template_name, context)

