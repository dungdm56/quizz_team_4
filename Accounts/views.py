"""
Author : FinalDevil
"""
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import login
from django.template import  RequestContext
from django.views.decorators.csrf import csrf_protect
from Class.models import Classes
from django.contrib.auth.models import User
from Accounts.models import RegistrationForm, EditProfileForm


@csrf_protect
def signup(request):
    """
    the definiton for signup method
    """
    if request.method == 'POST':
        # get form from request in web page
        form = RegistrationForm(request.POST)
        # check the validation of sign-up form
        if form.is_valid():
            # create new user with this data from form
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()  # save new user to the database
            return HttpResponseRedirect('/signup_success/')
    else:
        form = RegistrationForm()  # get form from models.py for web page
    # return a file html and some context for this file
    return render_to_response('registration/register.html',
                              context_instance=RequestContext(request,
                                {'form': form, 'User': request.user}))


def login_user(request):
    """
    The definition for login method
    """
    # get data for variable
    username = request.POST.get('username')
    password = request.POST.get('password')
    state = ''
    # check if the method of request is POST or not
    if request.POST:
        user = auth.authenticate(username=username, password=password)
        # check if the user is valid to login or not
        if user is not None and user.is_active:
            login(request, user)  # user method login of Python
            state = "You are successfully login"
            return HttpResponseRedirect('/home/')
        else:
            state = 'Sorry, that is not a valid name and or password'
            # return login page againt if the information is invalid
            return render_to_response('registration/login.html', {'state': state},
                context_instance=RequestContext(request, {'User': request.user}))
    else:
        # return login page if the method of request is not POST
        return render_to_response('registration/login.html', {'state': state},
            context_instance=RequestContext(request, {'User': request.user}))


def logout(request):
    """
    The definition for logout method
    """
    auth.logout(request)  # user logout method of Python
    return HttpResponseRedirect('/')


def home(request):
    """
    The definition for home method
    """
    return render_to_response('home.html',
        context_instance=RequestContext(request, {'User': request.user}))


def about(request):
    """
    The definition for about method
    """
    return render_to_response('about.html',
        context_instance=RequestContext(request, {'User': request.user}))


def signup_success(request):
    """
    The definition for signup_success method
    """
    return render_to_response('signup_success.html',
        context_instance=RequestContext(request, {'User': request.user}))


def member_list(request):
    """
    The definition for member_list method
    """
    return render_to_response('member_list.html',
        context_instance=RequestContext(request,
        {'User': request.user, 'member_list': User.objects.all()}))


def view_profile(request, member_id, member_username):
    """
    The definition for view_profile method
    """
    # get some variable for context of web page
    member = get_object_or_404(User, id=member_id, username=member_username)
    classes_list = Classes.objects.filter(user=member)
    return render_to_response('view_profile.html',
        context_instance=RequestContext(request,
            {'User': request.user, 'member': member, 'Classes_list': classes_list}))


def edit_profile(request):
    """
    The definition for edit_profile method
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        # check the form is valid or not
        if form.is_valid():
            form.save_data()  # save data from form
            return HttpResponseRedirect('/member/%s-%s/' %
                (request.user.id, request.user.username))
    else:
        form = EditProfileForm(instance=request.user)  # get form for webpage
    return render_to_response('edit/edit_profile.html',
        context_instance=RequestContext(request, {'User': request.user, 'form': form}))
