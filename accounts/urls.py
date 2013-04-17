'''
Created on Apr 1, 2013

@author: Admin
'''
from django.conf.urls import patterns, include, url
from accounts.views import member_list, view_profile, edit_profile

#url for account
urlpatterns = patterns('',
     url(r'^$', member_list),												#url to link with member_list in views.py
     url(r'^(?P<member_id>\d+)-(?P<member_username>\w+)/$', view_profile),	#url to link with view_profile in views.py
     url(r'^edit_my_profile/$', edit_profile),								#url to link with edit_profile in views.py
)
