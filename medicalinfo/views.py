from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from users.models import UserProfile, Employee, Doctor, Nurse
from medicalinfo.models import MedicalInformation
from django.contrib import messages
import datetime

from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required, permission_required
from accounts.views import trace_user

from medicalinfo.forms import (MedinfoInitForm, 
        ChronicMedicalProblemsForm, EmergencyContactForm, 
        InsuranceInformationForm, AllergenForm, CaseInitForm
)
# Create your views here.
def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

#security check to ensure patient can not view other patient med-info
def medinfo_security_check(request_user, ref_if):
    try:
        if request_user.patient:
            return request_user.userprofile.ref_id == ref_id
    except:
        #if user is not patient
        return True

#
#To view med-info of a patient
#
@permission_required('medicalinfo.read_medinfo', raise_exception=True)
def medinfo_view(request, ref_id):

    patient = trace_user(ref_id).patient

    #ensure patient cannot view other patients med-info
    if medinfo_security_check(request.user, ref_id):
        #check if the patient med-info is new
        if not patient.medicalinformation.initialized:
            messages.info(request, "You need to fill out this following form")
            #redirect patient to med-info init page
            return HttpResponseRedirect(reverse('med-info-init', kwargs={'ref_id':ref_id}))
        else:

            template_name= 'medicalinfo/medinfo_view_form.html'
            medinfo = patient.medicalinformation
            chronical_problems = medinfo.chronicmedicalproblems

 
            medinfo = patient.medicalinformation
            chronic = medinfo.chronicmedicalproblems
            emer = patient.emergencycontact
            insurance = patient.insuranceinformation
            allergen = medinfo.allergen

            #init form with instance

            form1 = MedinfoInitForm(instance=medinfo, prefix='med-info')
            form2 = ChronicMedicalProblemsForm(instance=chronic, prefix='chronical')
            form3 = EmergencyContactForm(instance=emer, prefix='emercontact')
            form4 = InsuranceInformationForm(instance=insurance, prefix='insurance')
            form5 = AllergenForm(instance=allergen)
      
            context = {'form1':form1, 'form2': list(form2), 'form3':form3, 'form4':form4, 'form5':form5}

            #messages.warning(request, "Opps, are you in the right place?")
            return render(request, template_name, context)
    else:
        return HttpResponseForbidden()


#
#Initilize a new med-info for a patient.
#
@permission_required('medicalinfo.init_medinfo', raise_exception=True)
def medinfo_init(request, ref_id):
    template_name= 'medicalinfo/medinfo_init_form.html'

    #ensure patient cannot init other patients med-info
    if medinfo_security_check(request.user, ref_id):

        patient = trace_user(ref_id).patient
        #get patient medicalinfo instance
        medinfo = patient.medicalinformation
        #init form with instance

        form1 = MedinfoInitForm(request.POST or None, instance=medinfo, prefix='med-info')
        form2 = ChronicMedicalProblemsForm(request.POST or None, prefix='chronical')
        form3 = EmergencyContactForm(request.POST or None, prefix='emercontact')
        form4 = InsuranceInformationForm(request.POST or None, prefix='insurance')
        form5 = AllergenForm(request.POST or None, prefix='allergen')

        if request.POST:
            if form1.is_valid() and form2.is_valid and form3.is_valid and form4.is_valid and form5.is_valid:
                medinfo = form1.save(commit=False)
                chronical_med_problems = form2.save(commit=False)
                chronical_med_problems.medinfo = medinfo

                emergency_contact = form3.save(commit=False)
                emergency_contact.patient = patient

                insurance = form4.save(commit=False)
                insurance.patient = patient

                allergen = form5.save(commit=False)
                allergen.medinfo = medinfo

                #change init status 
                medinfo.initialized = True

                #save to database
                medinfo.save()
                chronical_med_problems.save()
                emergency_contact.save()
                insurance.save()
                allergen.save()

                messages.success(request, "You have successfully updated your med-info")
                return HttpResponseRedirect(reverse('med-info-detail', kwargs={'ref_id':ref_id})) 
            else:
                messages.error(request, "Please correct the form")
        #messages.warning(request, "Opps, are you in the right place?")

        context = {'form1':form1, 'form2': list(form2), 'form3':form3, 'form4':form4, 'form5':form5}
        return render(request, template_name, context)
    else:
        return HttpResponseForbidden()


#
#Initilize a new med-info for a patient.
#
@permission_required('medicalinfo.init_case', raise_exception=True)
def diagnosis_init(request, ref_id):
    template_name= 'medicalinfo/medinfo_diagnosis_init_form.html'

    #ensure patient cannot init other patients med-info
    if medinfo_security_check(request.user, ref_id):

        patient = trace_user(ref_id).patient
        #get patient medicalinfo instance

        form1 = CaseInitForm(request.POST or None)
   
        if request.POST:
            if form1.is_valid():

                messages.success(request, "You have successfully updated your med-info")
                return HttpResponseRedirect(reverse('med-info-detail', kwargs={'ref_id':ref_id})) 
            else:
                messages.error(request, "Please correct the form")
        #messages.warning(request, "Opps, are you in the right place?")

        context = {'form1':form1}
        return render(request, template_name, context)
    else:
        return HttpResponseForbidden()



'''
@permission_required('medicalinfo.change_medicalinformation', raise_exception=True)
def medinfo_init(request, ref_id):
    template_name= 'medicalinfo/medinfo_init_form.html'
    context = {}


    patient = trace_user(ref_id).patient
    #get patient medicalinfo instance
    medinfo = patient.medicalinformation
    #init form with instance
    form = MedinfoInitForm(request.POST or None, instance=medinfo)
    if request.POST:
        if form.is_valid():
            medinfo = form.save(commit=False)
            #change init status 
            medinfo.initialized = True
            medinfo.save()
            messages.success(request, "You have successfully updated your med-info")
            return HttpResponseRedirect(reverse('med-info-detail', kwargs={'ref_id':ref_id})) 
        else:
            messages.error(request, "Please correct the form")
        #messages.warning(request, "Opps, are you in the right place?")

    context['form'] = form
    return render(request, template_name, context)

'''


@login_required(login_url='/account/login')
def userprofile_update(request, ref_id):
    '''check if request user is the same logged in user'''
    if check_user(request.user.userprofile.ref_id,ref_id):
        template_name = 'accounts/account_profile_udpate_form.html'
        

        context = {}
        profile = UserProfile.objects.get(ref_id=ref_id)
        form = UserProfileForm(request.POST or None, instance=profile)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully updated your profile information')
                return redirect('/account/message')

        context['form'] = form

        return render(request, template_name, context)
    else:
        template_name= 'accounts/account_message.html'
        patients = Patient.objects.all()
        context = {'patients' : patients}
        messages.warning(request, "Opps, are you in the right place?")
        return render(request, template_name, context)



