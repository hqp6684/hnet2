from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from users.models import UserProfile, Employee, Doctor, Nurse
from medicalinfo.models import MedicalInformation
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.decorators import login_required, permission_required
from accounts.views import trace_user

from medicalinfo.forms import (MedinfoInitForm, 
        ChronicMedicalProblemsForm, EmergencyContactForm, 
        InsuranceInformationForm, AllergenForm, CaseInitForm, CaseForm, PrescriptionForm,
)
from django.core.exceptions import PermissionDenied


from postman.api import pm_write


#trace user instance from patient doctor
def trace_doctor(patient):
    doc = patient.patient.primary_doctor.doctor.employee
    return doc

#System notification for medical information. 
#It will notify patient and patient's primary doctor
#** Need an account with username 'system'
def medical_system_notify(recipient, code, case):
    #recipient here is a patient
    sender = User.objects.get(username='system')
    primary_doctor = trace_doctor(recipient)

    if code=='new_case':
        subject = 'New case confirmation'
        body = _('Patient: %s \nP.Doctor: %s \nCase: %s')%(recipient.username, primary_doctor.username, case)
    elif code=='case_update':
        subject = 'Case update confirmation'
        body = _('Patient: %s \nP.Doctor: %s \nCase: %s\nA new update has been summitted')%(recipient.username, primary_doctor.username, case)
    elif code=='new_pres':
        subject = 'New prescription confirmation'
        body = _('Patient: %s \nP.Doctor: %s \nCase: %s\nA new prescription has been summitted')%(recipient.username, primary_doctor.username, case)

    pm_write(sender, recipient, subject=subject, body=body)
    pm_write(sender, recipient=primary_doctor, subject=subject, body=body)


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
            #forms     
            medinfo = patient.medicalinformation
            chronic = medinfo.chronicmedicalproblems
            emer = patient.emergencycontact
            insurance = patient.insuranceinformation
            allergen = medinfo.allergen

            #init form with instances

            form1 = MedinfoInitForm(request.POST or None, instance=medinfo, prefix='med-info')
            form2 = ChronicMedicalProblemsForm(request.POST or None, instance=chronic, prefix='chronical')
            form3 = EmergencyContactForm(request.POST or None, instance=emer, prefix='emercontact')
            form4 = InsuranceInformationForm(request.POST or None, instance=insurance, prefix='insurance')
            form5 = AllergenForm(request.POST or None, instance=allergen)
    
            if request.POST:
                if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
                    form1.save()
                    form2.save()
                    form3.save()
                    form4.save()
                    form5.save()

                    return HttpResponseRedirect(reverse('med-info-detail', kwargs={'ref_id':ref_id})) 
                else:
                    messages.error(request, "Please correct the form")
            #messages.warning(request, "Opps, are you in the right place?")

            context = {'form1':form1, 'form2': list(form2), 'form3':form3, 'form4':form4, 'form5':form5, 'ref_id':ref_id}

            #messages.warning(request, "Opps, are you in the right place?")
            return render(request, template_name, context)
    else:
        raise PermissionDenied

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
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
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
        raise PermissionDenied

#
#Initilize a new med-case
#
@permission_required('medicalinfo.read_medinfo', raise_exception=True)
def case_init(request, ref_id):
    template_name= 'medicalinfo/medinfo_new_case_form.html'

    #ensure patient cannot init other patients med-info
    if medinfo_security_check(request.user, ref_id):

        
        patient = trace_user(ref_id).patient
        #if patient is inactive (discharged)
        if not patient.is_active:
            raise PermissionDenied

        #get patient medicalinfo instance
        medinfo = patient.medicalinformation

        form1 = CaseInitForm(request.POST or None, initial={'medinfo': medinfo})
   
        if request.POST:
            if form1.is_valid():
                #create new case
                new_case = form1.save(commit=False)
                new_case.medinfo = medinfo
                new_case.save()
                #notify patient and its primary doctor
                recipient = trace_user(ref_id)
                medical_system_notify(recipient, code='new_case', case=new_case.problem)

                messages.success(request, "You have successfully summitted a new case")
                return HttpResponseRedirect(reverse('case-list-view', kwargs={'ref_id':ref_id})) 
            else:
                messages.error(request, "Please correct the form")
        #messages.warning(request, "Opps, are you in the right place?")

        context = {'form1':form1}
        return render(request, template_name, context)
    else:
        raise PermissionDenied

#
#Display all cases in a table
#
@permission_required('medicalinfo.read_medinfo', raise_exception=True)
def case_list_view(request, ref_id):
    template_name= 'medicalinfo/medinfo_case_list_view.html'

    #ensure patient cannot init other patients med-info
    if medinfo_security_check(request.user, ref_id):

        patient = trace_user(ref_id).patient
        #get patient medicalinfo instance
        medinfo = patient.medicalinformation

        cases = medinfo.case_set.all()

        context = {'cases':cases, 'ref_id':ref_id, 'patient':patient.patient.username}
        return render(request, template_name, context)
    else:
        raise PermissionDenied
#
#Case detail
#
@permission_required('medicalinfo.read_medinfo', raise_exception=True)
def case_detail_view(request, ref_id, case_id):
    template_name= 'medicalinfo/medinfo_case_detail_view_form.html'

    #ensure patient cannot init other patients med-info
    if medinfo_security_check(request.user, ref_id):

        patient = trace_user(ref_id).patient
        #get patient medicalinfo instance
        medinfo = patient.medicalinformation

        case = medinfo.case_set.get(id=case_id)

        form1 = CaseForm(request.POST or None, instance=case)

        prescriptions = case.prescription_set.all()


        context = {'form1':form1, 'view_only':True, 
            'ref_id':ref_id, 'case_id':case_id,
            'patient':patient.patient.username,
            'prescriptions':prescriptions,
            }

        return render(request, template_name, context)

    else:
        raise PermissionDenied
#
#Case update
#
@permission_required('medicalinfo.change_medicalinformation', raise_exception=True)
def case_update(request, ref_id, case_id):
    template_name= 'medicalinfo/medinfo_case_update_form.html'

    #ensure patient cannot init other patients med-info
    if medinfo_security_check(request.user, ref_id):

        patient = trace_user(ref_id).patient
        #get patient medicalinfo instance
        medinfo = patient.medicalinformation

        case = medinfo.case_set.get(id=case_id)

        prescriptions = case.prescription_set.all()

        form1 = CaseForm(request.POST or None, instance=case)

        if request.POST:
            if form1.is_valid():
                updated_case = form1.save(commit=False)
                updated_case.last_action = 'D'
                updated_case.save()
                messages.success(request, "You have successfully updated")
                medical_system_notify(trace_user(ref_id), code='case_update', case=case.problem) 
                return HttpResponseRedirect(reverse('case-detail-view', kwargs={'ref_id':ref_id, 'case_id':case_id})) 
            else:
                messages.error(request, "Please correct the form")           

        context = {'form1':form1, 'prescriptions':prescriptions}
        return render(request, template_name, context)
    else:
        raise PermissionDenied

#
#New Precription
#
@permission_required('medicalinfo.change_medicalinformation', raise_exception=True)
def case_update_prescription(request, ref_id, case_id):
    template_name= 'medicalinfo/medinfo_case_update_prescription_form.html'

    #ensure patient cannot init other patients med-info
    if medinfo_security_check(request.user, ref_id):

        patient = trace_user(ref_id).patient
        #get patient medicalinfo instance
        medinfo = patient.medicalinformation

        case = medinfo.case_set.get(id=case_id)
        prescriptions = case.prescription_set.all()

        form1 = CaseForm(request.POST or None, instance=case)
        form2 = PrescriptionForm(request.POST or None)

        if request.POST:
            if form2.is_valid():
                new_pres = form2.save(commit=False)
                new_pres.case = case
                new_pres.save()
                #updated last action on case
                case.last_action = 'P'
                case.save()
                messages.success(request, "You have successfully updated a prescription") 
                medical_system_notify(trace_user(ref_id), code='new_pres', case=case.problem)
                return HttpResponseRedirect(reverse('case-detail-view', kwargs={'ref_id':ref_id, 'case_id':case_id})) 
            else:
                messages.error(request, "Please correct the form")           

        context = {'form1':form1, 'form2':form2, 'prescriptions':prescriptions}
        return render(request, template_name, context)
    else:
        raise PermissionDenied



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
        raise PermissionDenied
