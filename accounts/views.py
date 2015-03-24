from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login

import datetime

from .forms import UserCreationForm, UserProfileForm, NewPatientForm, AuthenticationForm
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

def account_message(request, template_name='accounts/account-message.html'):
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


	template_name = 'accounts/account_patient_form.html'
	context = {'form1': form1, 'form2':form2}
	return render(request, template_name, context)

def account_login(request, template_name='accounts/account_login_form.html'):
    context = {}
    if request.user.is_authenticated():
    	messages.info(request, 'You have already logged in')
    	return redirect('/account/message')

    if request.method =='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request,form.get_user())
            messages.success(request, 'You have successfuly logged in')
            return redirect('/account/message')
    else:
        form = AuthenticationForm()
    context['form'] = form
    return render(request, template_name,context)


