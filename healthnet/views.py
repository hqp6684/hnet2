from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from users.models import UserProfile, Employee, Doctor, Nurse, Receptionist, Patient
from medicalinfo.models import MedicalInformation, InsuranceInformation
from django.contrib.auth.models import User

#custom 403 handler when permission_denied is raised
def http403(request, template_name='accounts/account_message.html'):
	context={}
	messages.warning(request, "Sorry, you don't have the permission to view this page. Please contact us for more information")
	return render(request,template_name, context)


def http404(request, template_name='home.html'):
	context={}
	messages.warning(request, "Oops")
	return render(request,template_name, context)

def home(request, template_name='home.html'):
	return render(request,template_name)

def index(request, template_name='index.html'):
	context = {}
	return render(request, template_name, context)

def contactus(request, template_name='contactus.html'):
	#set support = support username
	support_username = 'HN_support'
	context = {'support':support_username}
	return render(request, template_name, context)

def statistic(request):
	if not request.user.is_superuser:
		raise PermissionDenied
	template_name = 'statistic.html'

	users_total = User.objects.all().count() - 3
	non_patients = MedicalInformation.objects.filter(initialized=False).count()
	employees = Employee.objects.all().count()
	patients = MedicalInformation.objects.filter(initialized=True).count()

	no_insurance = InsuranceInformation.objects.filter(carrier='N').count()
	bluechoice = InsuranceInformation.objects.filter(carrier='B').count()
	united = InsuranceInformation.objects.filter(carrier='U').count()
	medicaid = InsuranceInformation.objects.filter(carrier='M').count()


	context = {'users_total':users_total,
		'non_patients':non_patients,
		'employees':employees,
		'patients':patients,
		'no_insurance':no_insurance,
		'bluechoice':bluechoice,
		'united':united,
		'medicaid':medicaid,

	}

	return render(request,template_name,context)
