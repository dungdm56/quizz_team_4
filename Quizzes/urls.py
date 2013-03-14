from django.conf.urls import patterns, include, url
from django.core.context_processors import csrf

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings
import os

static=os.path.join(
    os.path.dirname(__file__),'static'
)
image = os.path.join(
    os.path.dirname(__file__), 'image'
)


from accounts.views import login_user, logout, home, signup, about

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'Quizzes.views.home', name='home'),
    # url(r'^Quizzes/', include('Quizzes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', home),
	url(r'^home/$', home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login_user),
    url(r'^logout/$', logout),
    url(r'^register/$', signup),
    url(r'^about/$', about),
	
	
	
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': static }),

    (r'^image/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': image}),
)
