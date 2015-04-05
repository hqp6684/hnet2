from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.
from django.contrib import messages

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
	context = {}
	return render(request, template_name, context)
