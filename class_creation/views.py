from django.shortcuts import render_to_response, get_object_or_404
from class_creation.models import Classes, Quizzes, Questions
from  django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.http import Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext



from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from accounts.models import RegistrationForm
from django.contrib import auth
from django.contrib.auth import login

# Create your views here.
def Create_class(request):
    return render_to_response('class_creation/class_creation.html')