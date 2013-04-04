from django.shortcuts import render_to_response, get_object_or_404
from class_creation.models import Classes, Quizzes, Questions
from  django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.http import Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from django.core.exceptions import *
from django.utils import timesince


from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from accounts.models import RegistrationForm
from django.contrib import auth
from django.contrib.auth import login
from class_creation.models import *
from django.shortcuts import get_object_or_404
import datetime

# Create your views here.
def create_class(request):
    if request.method == 'POST':
        class_form = RegistrationClassForm(request.POST)
        if class_form.is_valid():
            Class =  Classes.objects.create(
                user = request.user,
                class_name = class_form.cleaned_data['class_name'],
                number_students = class_form.cleaned_data['number_students'],
                teacher_name = class_form.cleaned_data['teacher_name'],
                Update_time = datetime.datetime.now(),
                Update_date = datetime.datetime.now()
            )
            Class.save()
            return HttpResponseRedirect('/create_class_success/'+str(Class.id)+'/')
    else:
        class_form = RegistrationClassForm()
    return render_to_response('class_creation/class_creation.html',context_instance=RequestContext(request,{'class_form':class_form, 'User': request.user}))

def create_class_success(request,id_class):
    Class1 = get_object_or_404(Classes,id = id_class)
    return render_to_response('class_creation/class_creation_success.html',context_instance=RequestContext(request,{ 'User': request.user,'Classes_list':Class1}))

def classes(request,id_class):
    Class1 = get_object_or_404(Classes,id = id_class)
    Quizz = Quizzes.objects.filter(Class = Class1)
    return render_to_response('class.html',context_instance=RequestContext(request,{ 'User': request.user,'Classes_list':Class1,'Quizzes_list':Quizz}))

def edit_class(request,id_class):
    Class1 = get_object_or_404(Classes,id = id_class)
    if request.POST :
        if not Class1.class_name == request.POST.get('class_name') :
            class_form = RegistrationClassForm(request.POST)
        else :
            class_form = RegistrationClassForm2(request.POST)
        if class_form.is_valid():
            Class1.user = request.user
            Class1.class_name = request.POST.get('class_name')
            Class1.number_students = request.POST.get('number_students')
            Class1.teacher_name = request.POST.get('teacher_name')
            Class1.save()
            return HttpResponseRedirect('/class/'+str(Class1.id)+'/')
    return render_to_response('edit/edit_class.html',context_instance=RequestContext(request,{ 'User': request.user,'Classes_list':Class1}))

def create_quizz(request,id_class):
    Classes_list = Classes.objects.filter(user = request.user.id)
    Class1 = get_object_or_404(Classes,id = id_class)
    if request.method == 'POST':
        form = MakeQuizzForm(request.POST)
        if form.is_valid():
            Quizz = Quizzes.objects.create(
                Class = Class1,
                Title = form.cleaned_data['Title'],
                Time_limit = form.cleaned_data['Time_limit'],
                Update_time = datetime.datetime.now(),
                Update_date = datetime.datetime.now(),
                Number_questions = 0
                )
            Quizz.save()
            return HttpResponseRedirect('/class/'+str(Quizz.Class.id)+'/')
    else :
        form = MakeQuizzForm()
    return render_to_response('class_creation/quizzes_creation.html', context_instance = RequestContext(request,{'form':form,'User':request.user,'Classes_list':Classes_list}))

def make_quizzes_success(request):
    return render_to_response('class_creation/make_quizzes_success.html',context_instance=RequestContext(request,{ 'User': request.user}))

def quizzes(request,id_quizz):
    Quizz = get_object_or_404(Quizzes,id = id_quizz)
    Questions_list = Questions.objects.filter(quizz = Quizz)
    return render_to_response('quizzes.html',context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':Quizz,'Questions_list':Questions_list}))

def create_question(request,id_quizz):
    state = ' '
    Quizz = get_object_or_404(Quizzes,id = id_quizz)
    Question = request.POST.get('Ques')
    Answer1 = request.POST.get('Ans1')
    Answer2 = request.POST.get('Ans2')
    Answer3 = request.POST.get('Ans3')
    Answer4 = request.POST.get('Ans4')
    Correct_answer = request.POST.get('correct_ans')
    if request.method == 'POST':
        if Question and Answer1 and Answer2 and Answer3 and Answer4 and Correct_answer:
            Question = Questions.objects.create(
                quizz = Quizz,
                Ques = Question,
                Ans1 = Answer1,
                Ans2 = Answer2,
                Ans3 = Answer3,
                Ans4 = Answer4,
                Correct_ans = Correct_answer
                )
            Question.save()
            Quizz.Number_questions = Quizz.Number_questions + 1
            Quizz.save()
            return HttpResponseRedirect('/quizzes/'+str(Question.quizz.id)+'/')
        else :
            state = 'Please enter all information'
    return render_to_response('class_creation/questions_creation.html',{'state':state},context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':Quizz}))

def doing_quizz(request,id_quizz):
    Quizz = get_object_or_404(Quizzes,id = id_quizz)
    Questions_list = Questions.objects.filter(quizz = Quizz)
    if request.POST:
        leng = len(Questions_list)
        mark = leng
        empty = 0
        for Question in Questions_list:
            answer = 'Answer'+str(Question.id)
            if request.POST.get(answer) is not None:
                if not str(Question.Correct_ans) == str(request.POST.get(answer)):
                    mark = mark - 1
            else :
                empty = empty +1
                mark = mark - 1
        return HttpResponseRedirect('/result/'+str(Quizz.id)+'/'+str(mark)+'/'+str(empty)+'/')
    return render_to_response('doing_quizzes.html',context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':Quizz,'Questions_list':Questions_list}))
    
def result(request,id_quizz,val_mark,val_empty):
    Quizz = get_object_or_404(Quizzes,id = id_quizz)
    Questions_list = Questions.objects.filter(quizz = Quizz)
    leng = len(Questions_list)
    mark = int(val_mark)
    empty = int(val_empty)
    wrong = leng - mark - empty
    percent = int(((float(int(float(mark)/float(leng)*100)))/100) *100)
    return render_to_response('result.html',context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':Quizz,'mark':mark,'leng':leng,'empty':empty,'wrong':wrong,'percent':percent}))

def answer(request,id_quizz):
    Quizz = get_object_or_404(Quizzes,id = id_quizz)
    Questions_list = Questions.objects.filter(quizz = Quizz)
    return render_to_response('answer.html',context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':Quizz,'Questions_list':Questions_list}))