from django.conf.urls import patterns, url
from scheduling.views import *

urlpatterns = patterns('',
	url(r'^calendar/(?P<year>\d{4})/(?P<month>\d{1,2})/$', calendar, name="calendar"),
    url(r'^appointment/create/$', appointment_create, name = 'appointment-create'),
    url(r'^appointment/(?P<pk>\d+)/$', AppointmentDetailView.as_view(), name='appointment-detail'),
    url(r'^appointment/(?P<apt_id>\d+)/update/$', appointment_update, name='appointment-update'),
    url(r'^appointment/(?P<pk>\d+)/delete/$', AppointmentDeleteView.as_view(), name='appointment-delete'),
    #url(r'^appointment/(?P<message_id>[\d]+)/edit/&', AppointmentEdit.as_view(), 'appointment-edit'),
    #url(r'^appointment/(?P<message_id>[\d]+)/delete/&', AppointmentDelete.as_view(), 'appointment-delete'),



)