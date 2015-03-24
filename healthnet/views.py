from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.

def home(request, template_name='home.html'):
	return render(request,template_name)

def index(request, template_name='index.html'):
	context = {}
	return render(request, template_name, context)
