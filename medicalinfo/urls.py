from django.conf.urls import patterns, url
from medicalinfo import views

urlpatterns = patterns('',
	url(r'^$', views.index),
	#url(r'^register/$', views.patient_register, name='patient-register'),

	url(r'^(?P<ref_id>[\w]+)/initializing/$', views.medinfo_init,name='med-info-init'),
	url(r'^(?P<ref_id>[\w]+)/new-case/$', views.case_init,name='case-init'),
	url(r'^(?P<ref_id>[\w]+)/cases/(?P<case_id>[\d]+)/new-prescription/$', views.case_update_prescription,name='case-update-prescription'),
	url(r'^(?P<ref_id>[\w]+)/cases/(?P<case_id>[\d]+)/update/$', views.case_update,name='case-update'),

	url(r'^(?P<ref_id>[\w]+)/cases/(?P<case_id>[\d]+)$', views.case_detail_view,name='case-detail-view'),

	url(r'^(?P<ref_id>[\w]+)/cases/$', views.case_list_view,name='case-list-view'),

	
	#url(r'^(?P<ref_id>[\w]+)/new-case/$', views.diagnosis_init,name='case-init'),


	url(r'^(?P<ref_id>[\w]+)/$', views.medinfo_view,name='med-info-detail'),
	#url(r'^(?P<ref_id>[\w]+)/update/$', views.userprofile_update, name='userprofile-update'),

)