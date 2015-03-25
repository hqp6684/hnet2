from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
	#url(r'^$', views.index),
	url(r'^register/$', views.patient_register, name='patient-register'),
	url(r'^employee-register/$', views.employee_register, name='employee-register'),

	url(r'^message/$', views.account_message, name='account-message'),
	url(r'^login/$', views.account_login, name='account-login'),
	url(r'^logout/$', views.account_logout, name='account-logout'),
	
	url(r'^(?P<ref_id>[\w]+)/$', views.userprofile_view, name='userprofile-detail'),
	url(r'^(?P<ref_id>[\w]+)/update/$', views.userprofile_update, name='userprofile-update'),




)