from django.shortcuts import render_to_response, get_object_or_404
from class_creation.models import Classes, Quizzes, Questions
from  django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.http import Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from django.core.exceptions import *


from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from accounts.models import RegistrationForm
from django.contrib import auth
from django.contrib.auth import login
from class_creation.models import RegistrationClassForm
from class_creation.models import MakeQuizzForm
from django.shortcuts import get_object_or_404

# Create your views here.
def create_class(request):
    if request.method == 'POST':
        class_form = RegistrationClassForm(request.POST)
        if class_form.is_valid():
            Class =  Classes.objects.create(
                user = request.user,
                class_name = class_form.cleaned_data['class_name'],
                number_students = class_form.cleaned_data['number_students'],
                teacher_name = class_form.cleaned_data['teacher_name']
            )
            Class.save()
            return HttpResponseRedirect('/create_class_success/'+str(Class.id)+'/')
    else:
        class_form = RegistrationClassForm()
    return render_to_response('class_creation/class_creation.html',context_instance=RequestContext(request,{'class_form':class_form, 'User': request.user}))

def create_class_success(request,id_class):
    Class = get_object_or_404(Classes,id = id_class)
    Class1 = Classes.objects.filter(id = id_class)
    return render_to_response('class_creation/class_creation_success.html',context_instance=RequestContext(request,{ 'User': request.user,'Classes_list':Class1}))

def classes(request,id_class):
    Class = get_object_or_404(Classes,id = id_class)
    Class1 = Classes.objects.filter(id = id_class)
    return render_to_response('class.html',context_instance=RequestContext(request,{ 'User': request.user,'Classes_list':Class1}))



def create_quizz(request):
    if request.method == 'POST':
        form = MakeQuizzForm(request.POST)
        if form.is_valid():
            Quizz = Quizzes.objects.create(
                Class = request.POST['Class'],
                Title = form.cleaned_data['Title'],
                Time_limit = form.cleaned_data['Time_limit']
                )
            Quizz.save()
            return HttpResponseRedirect('/make_quizzes_success/')
    else :
        form = MakeQuizzForm()
    Classes_list = Classes.objects.filter(user = request.user.id)
    return render_to_response('class_creation/quizzes_creation.html', context_instance = RequestContext(request,{'form':form,'User':request.user,'Classes_list':Classes_list}))

def make_quizzes_success(request):
    return render_to_response('class_creation/make_quizzes_success.html',context_instance=RequestContext(request,{ 'User': request.user}))




