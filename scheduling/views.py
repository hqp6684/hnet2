from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from users.models import Patient, Doctor, is_doctor, is_employee, is_patient, is_nurse, User
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.edit import HttpResponseRedirect, UpdateView, DeleteView
from scheduling.forms import AppointmentForm
from scheduling.models import AppointmentCalendar, Appointment
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import date
from django.http import HttpResponse
from django.contrib import messages
from postman.api import pm_write

'''
View monthly calendar.
@:param year - desired year.
@:param month - desired month.
'''
@login_required(login_url='/account/login')
def calendar(request, year, month):
    year =  int(year)
    month = int(month)
    if is_patient(request.user):
        #get apts for patient
        my_appointments = Appointment.objects.order_by('start_time').filter(start_time__year=year, start_time__month=month, patient = request.user)
    elif is_employee(request.user):

        if is_doctor(request.user):
            #get apts for doctor
            my_appointments = Appointment.objects.order_by('start_time').filter(start_time__year=year, start_time__month=month, doctor = request.user)
        else:
            #get apts for nurse/receptionist
            my_appointments = Appointment.objects.order_by('start_time').filter(start_time__year=year, start_time__month=month)
    else:
        # get apts for admin
         my_appointments = Appointment.objects.order_by('start_time').filter(start_time__year=year, start_time__month=month)

    cal_object = AppointmentCalendar(my_appointments)
    cal = cal_object.formatmonth(year, month)

    return render(request, 'calendar_template.html', {'calendar': mark_safe(cal), 'cal_object':cal_object})

"""
Notify patients and doctors of appointment related activities.
"""
def apt_system_notify(patient, doctor, code):
    sender = User.objects.get(username='system')

    #**You need an account named 'system', so either register new user by Admin console
    #**or by django API (shell). If you dont like 'system', you can change system to anything, then create
    #**account with that name

    if code=='new_apt':
        subject = 'New Appointment Confirmation'
        body = 'A new appointment has been scheduled for %s with doctor %s' %(patient.patient.username,doctor.doctor.employee.username)

    pm_write(sender, recipient=patient.patient, subject=subject, body=body)
    pm_write(sender, recipient=doctor.doctor.employee, subject=subject, body=body)



'''
Create new appointment.
'''
@login_required(login_url='/account/login')
def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            apt = form.save(commit=False)
            apt_system_notify(apt.patient, apt.doctor, 'new_apt')
            apt.save()
            messages.success(request, 'You have successfully made an appointment')

            return HttpResponseRedirect(reverse('calendar', kwargs={"month": date.today().month, "year": date.today().year}))
        else:
            messages.error(request, "Please correct the form")


    else:
        form = AppointmentForm()
        form.set_query_sets(request.user)

    return render_to_response('appointment_create.html',
        {'form': form, },
        context_instance=RequestContext(request))

''' 
View appointment details.
'''
class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "appointment_detail.html"


'''
Update an existing appointment.
@:param id of appointment to update.
'''
@login_required(login_url='/account/login')
def appointment_update(request, apt_id):
    apt = get_object_or_404(Appointment, pk = apt_id)

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=apt)
        if form.is_valid():
            apt = form.save(commit=False)
            #apt.start_time = request.POST['start_time']
            #apt.end_time = request.POST['end_time']
            apt.save()
            return HttpResponseRedirect(reverse('calendar', kwargs={"month": date.today().month, "year": date.today().year}))
        else:
            messages.error(request, "Please correct the form")


    else:


        if (apt!=None):
            if is_patient(request.user):
                if apt.patient != request.user.patient:
                    return HttpResponse(status=403)
            if is_doctor(request.user):
                if apt.doctor != request.user.employee.doctor:
                    return HttpResponse(status=403)

        form = AppointmentForm(instance=apt)

        form.set_query_sets(request.user)

    return render_to_response('appointment_create.html',
        {'form': form, },
        context_instance=RequestContext(request))


'''
Delete an appointment.
'''
class AppointmentDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('calendar', kwargs = {"year": date.today().year, "month": date.today().month})
    template_name = 'appointment_delete.html'