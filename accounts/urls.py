from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
	#url(r'^$', views.index),
	url(r'^register/$', views.patient_register, name='patient-register'),
	url(r'^employee-register/$', views.employee_register, name='employee-register'),
	url(r'^employee-management/list/$', views.employee_list_view, name='employee-list'),
	url(r'^employee-management/(?P<ref_id>[\w]+)/update/$', views.employee_update_view, name='employee-update'),

	url(r'^message/$', views.account_message, name='account-message'),
	url(r'^login/$', views.account_login, name='account-login'),
	url(r'^logout/$', views.account_logout, name='account-logout'),
	
	url(r'^(?P<ref_id>[\w]+)/$', views.userprofile_view,name='userprofile-detail'),
	url(r'^(?P<ref_id>[\w]+)/update/$', views.userprofile_update, name='userprofile-update'),

	url(r'^patient-inactive-list/$', views.patient_inactive_list_view, name='patient-inactive-list'),
	url(r'^my-patients/$', views.my_patient_list_view, name='my-patient-list'),
	url(r'^my-patients/archive/$', views.all_my_patient_list_view, name='my-patient-list-archive'),

	url(r'^patient-list/(?P<ref_id>[\w]+)/$', views.patient_activate, name='patient-activate'),
	url(r'^patient-list/(?P<ref_id>[\w]+)/discharge/$', views.patient_discharge, name='patient-discharge'),
	url(r'^patient-list/(?P<ref_id>[\w]+)/transfer/$', views.patient_transfer, name='patient-transfer'),
	url(r'^patient-list/(?P<ref_id>[\w]+)/add-doctor/$', views.patient_add_doctor, name='patient-add-doctor'),



)
