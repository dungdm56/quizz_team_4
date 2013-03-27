from django.conf.urls import patterns, include, url

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
from class_creation.views import create_class

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'Quizzes.views.home', name='home'),
    url(r'^creat_class/', create_class),

)
