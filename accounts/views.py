# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from accounts.models import RegistrationForm, EditProfileForm
from django.contrib import auth
from django.contrib.auth import login
from django.template import  RequestContext
from django.views.decorators.csrf import csrf_protect
from class_creation.models import Classes
from django.contrib.auth.models import User


@csrf_protect

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            user.save()
            return HttpResponseRedirect('/signup_success/')
    else:
        form = RegistrationForm()
    # return render(request,'steps_count/index.html',{'top_list': top_list})
    return render_to_response('registration/register.html', context_instance=RequestContext(request, {'form' : form, 'user': request.user}))

def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    state = ''
    if request.POST:
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            state = "You are successfully login"
            return HttpResponseRedirect('/home/')
        else:
            state = 'Sorry, that is not a valid name and or password'
            return render_to_response('registration/login.html', {'state':state}, context_instance=RequestContext(request, { 'user': request.user}))
    else:
        return render_to_response('registration/login.html', {'state':state}, context_instance=RequestContext(request, { 'user': request.user}))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request, { 'user': request.user}))

def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request, { 'user': request.user}))
def signup_success(request):
    return render_to_response('signup_success.html', context_instance=RequestContext(request, { 'user': request.user}))

def member_list(request):
    return render_to_response('member_list.html',
        context_instance=RequestContext(request, {'user': request.user, 'member_list': User.objects.all()}))

def view_profile(request, member_id, member_username):
    member = get_object_or_404(User, id=member_id, username=member_username)
    classes_list = Classes.objects.filter(user = member)
    return render_to_response('view_profile.html',
        context_instance=RequestContext(request, {'User': request.user, 'member': member,'Classes_list':classes_list}))

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save_data()
            return HttpResponseRedirect('/member/%s-%s/' % (request.user.id, request.user.username))
    else:
        form = EditProfileForm(instance=request.user)
    return render_to_response('edit/edit_profile.html',
            context_instance=RequestContext(request, {'User': request.user, 'form': form}))
