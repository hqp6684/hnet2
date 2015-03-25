from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import UserProfile, Employee, Doctor
from django.contrib import messages
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
import datetime

from .forms import (UserCreationForm, UserProfileForm, 
	NewPatientForm, AuthenticationForm, EmployeeCreationForm

)

from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

''' create a random reference id for user'''
import uuid
def get_ref_id():
	ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
	print ("get id %s") %ref_id
	try:
		id_exist = UserProfile.objects.get(ref_id=ref_id)
		get_ref_id()
	except:
		return ref_id

def account_message(request, template_name='accounts/account_message.html'):
	context = {}
	return render(request, template_name, context)

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
			#save user profile to database
			profile.save()
			#create new employee instance
			new_employee = form3.save(commit=False)
			#set related user
			new_employee.employee = user
			new_employee.save()
			if new_employee.employee_type == 'D':
				new_doc = Doctor.create(new_employee)
				new_doc.save()
				messages.success(request, 'A doctor has been registered')
				#return to home 
				return redirect('/account/message')
			else:
				messages.error(request, 'something wrong')
		else:
			messages.error(request, 'Please correct all the fields with error')


	template_name = 'accounts/account_employee_register_form.html'
	context = {'form1': form1, 'form2':form2, 'form3':form3}
	return render(request, template_name, context)

def account_login(request, 
	template_name='accounts/account_login_form.html'):

    context = {}
    if request.user.is_authenticated():
    	messages.info(request, 'You have already logged in')
    	return redirect('/account/message')

    if request.method =='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            messages.success(request, 'You have successfully logged in')
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

def check_user(request_ref_id, ref_id):
	return request_ref_id == ref_id

@login_required(login_url='/account/login')
def userprofile_view(request, ref_id):
	'''check if request user is the same logged in user'''
	if check_user(request.user.userprofile.ref_id,ref_id):
		template_name = 'accounts/account_profile_view_form.html'
		context = {}
		profile = UserProfile.objects.get(ref_id=ref_id)
		context['profile'] = profile
		return render(request, template_name, context)
	else:
		template_name= 'accounts/account_message.html'
		context = {}
		messages.warning(request, "Opps, are you in the right place?")
		return render(request, template_name, context)


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
		context = {}
		messages.warning(request, "Opps, are you in the right place?")
		return render(request, template_name, context)



