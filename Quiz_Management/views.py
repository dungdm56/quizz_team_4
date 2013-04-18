'''
Created on Mar 22, 2013

@author: NVDAI
'''
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth import login
from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect
from Class.models import Classes
from Accounts.models import RegistrationForm

@csrf_protect
# the definition for home method
def home(request):
    # check if the user is valid or not
    if request.user is not None :
        # get some variable for context in web page
        classes_list = Classes.objects.filter(user=request.user.id)
        classes_list_joined = Classes.objects.filter(students=request.user.id)
        classes_list_another = Classes.objects.all()
        # return home.html and some context
        return render_to_response('home.html', context_instance=RequestContext(request, {'User':request.user, 'classes_list':classes_list, 'classes_list_another':classes_list_another, 'classes_list_joined':classes_list_joined}))
    else :
        return render_to_response('home.html', context_instance=RequestContext(request, {'User':request.user}))  # return home.html and some context
