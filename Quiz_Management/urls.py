from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import os

static = os.path.join(
    os.path.dirname(__file__), 'static'
)
image = os.path.join(
    os.path.dirname(__file__), 'image'
)

from Accounts.views import login_user, logout, signup, about, signup_success
from Class.views import create_class, create_class_success, classes, edit_class
from Quizz.views import *
from Quiz_Management.views import home

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	# home
    url(r'^$', home),
	url(r'^home/$', home),
    url(r'^about/$', about),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': static }),

    (r'^image/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': image}),
)

# account
urlpatterns += patterns('Accounts.views',
    url(r'^login/$', login_user),
    url(r'^logout/$', logout),
    url(r'^register/$', signup),
    url(r'./register/$', signup),
    url(r'^signup_success/$', signup_success),
    url(r'^member/', include('Accounts.urls')),
)

# classes
urlpatterns += patterns('',
    url(r'^class/([^\s]+)/$', classes),
    url(r'^create_class/$', create_class),
    url(r'^create_class_success/([^\s]+)/$', create_class_success),
    url(r'^edit_class/([^\s]+)/$', edit_class),
)

# quizzes
urlpatterns += patterns('',
    url(r'^create_quizz/([^\s]+)/$', create_quizz),
    url(r'^quizzes/([^\s]+)/$', quizzes),
    url(r'^doing_quizz/([^\s]+)/$', doing_quizz),
    url(r'^edit_quizz/([^\s]+)/$', edit_quizz),
)

# question and result
urlpatterns += patterns('',
    url(r'^create_questions/([^\s]+)/$', create_question),
    url(r'^edit_question/([^\s]+)/$', edit_question),
    url(r'^delete_question/([^\s]+)/$', delete_question),
    url(r'^result/([^\s]+)/([^\s]+)/([^\s]+)/([^\s]+)/$', result),
    url(r'^answer/([^\s]+)/$', answer),
)
