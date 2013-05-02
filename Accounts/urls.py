'''
Created on Apr 1, 2013

@author: Admin
'''
from django.conf.urls import patterns, url
from Accounts.views import member_list, view_profile, edit_profile

# url for account
urlpatterns = patterns('',
     url(r'^$', member_list),
     url(r'^(?P<member_id>\d+)-(?P<member_username>\w+)/$', view_profile),
     url(r'^edit_my_profile/$', edit_profile),
)
