# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from accounts.models import RegistrationForm
from django.contrib import auth
from django.contrib.auth import login
from django.core.context_processors import csrf
from django.template import Context, loader, RequestContext

from django.views.decorators.csrf import csrf_protect

@csrf_protect

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user =  User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email']
            )
            user.save()
        return HttpResponseRedirect('/singup_success/')
    else:
        form = RegistrationForm(request.POST)
       #  return render(request,'steps_count/index.html',{'top_list': top_list})
        return render_to_response('registration/register.html', {'form' : form}, context_instance=RequestContext(request) )

def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    state = ''
    if request.POST:
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            login(request, user)
            state = "You are successfully login"
            return HttpResponseRedirect('create_class')
        else:
            state = 'Sorry, that is not a valid name and or password'
            return render_to_response('registration/login.html',{'state':state},  context_instance=RequestContext(request))
    else:
        return render_to_response('registration/login.html',{'state':state}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
