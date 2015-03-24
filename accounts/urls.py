from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
	#url(r'^$', views.index),
	url(r'^register/$', views.patient_register, name='patient-register'),
	url(r'^message/$', views.account_message, name='account-message'),
	url(r'^login/$', views.account_login, name='account-login'),
	





)