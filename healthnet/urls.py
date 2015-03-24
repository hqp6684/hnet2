from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    
    # url(r'^blog/', include('blog.urls')),
    url(r'^index', 'healthnet.views.index', name='index'),
    
    url(r'^admin/', include(admin.site.urls), name='admin-site'),
    #users
    url(r'^users/', include('users.urls')),
    #
    url(r'^account/', include('accounts.urls')),

	url(r'^$', 'healthnet.views.home', name='home'),
)
