from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #message system
    url(r'^messages/', include('postman.urls')),

    # url(r'^blog/', include('blog.urls')),
    url(r'^index', 'healthnet.views.index', name='index'),
    
    url(r'^admin/', include(admin.site.urls), name='admin-site'),
    #users
    url(r'^users/', include('users.urls')),
    #
    url(r'^account/', include('accounts.urls')),
    url(r'^medicalinfomation/', include('medicalinfo.urls'), name='med-info'),

    
    url(r'^contactus/$', 'healthnet.views.contactus', name='contactus'),
    url(r'^statistic/$', 'healthnet.views.statistic', name='statistic-home'),

	url(r'^$', 'healthnet.views.home', name='home'),

    url(r'^schedule/', include('scheduling.urls')),

)

handler403 = 'healthnet.views.http403'
handler404 = 'healthnet.views.http404'
