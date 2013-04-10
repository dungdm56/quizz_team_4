
from django.template import RequestContext

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from class_creation.models import RegistrationClassForm, Classes, Quizzes, CheckInformationOfClass, MakeQuizzForm, Questions

from django.shortcuts import get_object_or_404
import datetime

# Create your views here.
#=======create new class===============================================
def create_class(request):
    if request.method == 'POST':
        class_form = RegistrationClassForm(request.POST)
        if class_form.is_valid():
            new_class =  Classes.objects.create(
                user = request.user,
                class_name = class_form.cleaned_data['class_name'],
                number_students = class_form.cleaned_data['number_students'],
                teacher_name = class_form.cleaned_data['teacher_name'],
                update_time = datetime.datetime.now(),
                update_date = datetime.datetime.now()
            )
            new_class.save()
            return HttpResponseRedirect('/create_class_success/'+str(new_class.id)+'/')
    else:
        class_form = RegistrationClassForm()
    return render_to_response('class_creation/class_creation.html',context_instance=RequestContext(request,{'class_form':class_form, 'User': request.user}))


#=======when you create new class successful============================
def create_class_success(request,id_class):
    _class = get_object_or_404(Classes,id = id_class)
    return render_to_response('class_creation/class_creation_success.html',context_instance=RequestContext(request,{ 'User': request.user,'Classes_list':_class}))


#=======the return when you visit any class=============================
def classes(request,id_class):
    _class = get_object_or_404(Classes,id = id_class)
    quizz = Quizzes.objects.filter(in_class = _class)
    list_user = User.objects.exclude(username = request.user.username)
    if request.POST.get('add_students') :
        student = User.objects.get(id = request.POST.get('add_students'))
        _class.students.add(student)
        _class.save()
    if request.POST.get('students_delete'):
        list_students = request.POST.getlist('students_delete')
        for name in list_students:
            student = User.objects.get(username = name)
            _class.students.remove(student)
        _class.save()
    students = _class.students.all()
    length = len(students)
    return render_to_response('class.html',context_instance=RequestContext(request,{ 'User': request.user,'Classes':_class,'Quizzes_list':quizz,'list_user':list_user,'list_students':students,'length':length}))

#=======when you want to edit your class================================
def edit_class(request,id_class):
    _class = get_object_or_404(Classes,id = id_class)
    if request.POST :
        if not _class.class_name == request.POST.get('class_name'):
            class_form = RegistrationClassForm(request.POST)
        else :
            class_form = CheckInformationOfClass(request.POST)
        if class_form.is_valid():
            _class.user = request.user
            _class.class_name = request.POST.get('class_name')
            _class.number_students = request.POST.get('number_students')
            _class.teacher_name = request.POST.get('teacher_name')
            _class.save()
            return HttpResponseRedirect('/class/'+str(_class.id)+'/')
    return render_to_response('edit/edit_class.html',context_instance=RequestContext(request,{ 'User': request.user,'Classes':_class}))


#=======when you want to create quizzes for your class===================
def create_quizz(request,id_class):
    classes_list = Classes.objects.filter(user = request.user.id)
    in_class = get_object_or_404(Classes,id = id_class)
    
    if request.method == 'POST':
        form = MakeQuizzForm(request.POST)
        if form.is_valid():
            quizz = Quizzes.objects.create(
                in_class = in_class,
                title = form.cleaned_data['title'],
                time_limit = form.cleaned_data['time_limit'],
                update_time = datetime.datetime.now(),
                update_date = datetime.datetime.now(),
                number_questions = 0,
            )
            quizz.save()
            return HttpResponseRedirect('/class/'+str(quizz.in_class.id)+'/')
    else :
        form = MakeQuizzForm()
    return render_to_response('class_creation/quizzes_creation.html', context_instance = RequestContext(request,{'form':form,'User':request.user,'classes_list':classes_list}))

#==========When you want to edit quizz====================================
def edit_quizz(request,id_quizz):
    quizz = get_object_or_404(Quizzes,id = id_quizz)
    class_of_quizz= quizz.in_class
    if request.POST :
		quizz_form = MakeQuizzForm(request.POST)
		
		if quizz.title == request.POST.get('title'):
			quizz.time_limit= request.POST.get('time_limit')
			quizz.save()
			return HttpResponseRedirect('/quizzes/'+str(quizz.id)+'/')
		
		if quizz_form.is_valid():
			quizz.title= request.POST.get('title')
			quizz.time_limit= request.POST.get('time_limit')
			quizz.save()
			return HttpResponseRedirect('/quizzes/'+str(quizz.id)+'/')
    return render_to_response('edit/edit_quizz.html',context_instance=RequestContext(request,{ 'User': request.user, 'Quizz': quizz, 'Classes':class_of_quizz}))



#=========the return when you want to visit a quizz page===================
def quizzes(request,id_quizz):
    quizz = get_object_or_404(Quizzes,id = id_quizz)
    questions_list = Questions.objects.filter(quizz = quizz)
    students = quizz.in_class.students.all()
    return render_to_response('quizzes.html',context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':quizz,'questions_list':questions_list,'list_students':students}))

#=========when you want to create questions for your quizzes===============
def create_question(request,id_quizz):
    state = ' '
    quizz = get_object_or_404(Quizzes,id = id_quizz)
    question = request.POST.get('ques')
    answer1 = request.POST.get('ans1')
    answer2 = request.POST.get('ans2')
    answer3 = request.POST.get('ans3')
    answer4 = request.POST.get('ans4')
    correct_answer = request.POST.get('correct_ans')
    if request.method == 'POST':
        if question and answer1 and answer2 and answer3 and answer4 and correct_answer:
            question = Questions.objects.create(
                quizz = quizz,
                ques = question,
                ans1 = answer1,
                ans2 = answer2,
                ans3 = answer3,
                ans4 = answer4,
                correct_ans = correct_answer
                )
            question.save()
            quizz.number_questions = quizz.number_questions + 1
            quizz.save()
            return HttpResponseRedirect('/quizzes/'+str(question.quizz.id)+'/')
        else :
            state = 'Please enter all information'
    return render_to_response('class_creation/questions_creation.html',{'state':state},context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':quizz}))

#==========When you want to edit question===========================
def edit_question(request,id_question):
	question = get_object_or_404(Questions,id = id_question)
	state = ' '
	in_quizz = question.quizz
	ques = request.POST.get('ques')
	answer1 = request.POST.get('ans1')
	answer2 = request.POST.get('ans2')
	answer3 = request.POST.get('ans3')
	answer4 = request.POST.get('ans4')
	correct_ans = request.POST.get('correct_ans')
	
	if request.method == 'POST':
		if ques and answer1 and answer2 and answer3 and answer4 and correct_ans:
				quizz = in_quizz
				question.ques = ques
				question.ans1 = answer1
				question.ans2 = answer2
				question.ans3 = answer3
				question.ans4 = answer4
				question.correct_ans = correct_ans
				question.save()
				quizz.save()
				return HttpResponseRedirect('/quizzes/'+str(question.quizz.id)+'/')
		else :
			state = 'Please enter all information'
			
	return render_to_response('edit/edit_question.html',{'state':state},context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':in_quizz, 'Question': question}))

#==========When you want to delete question===============================
def delete_question(request, id_question):
    question= get_object_or_404(Questions, id= id_question)
    quizz= question.quizz
    quizz.number_questions= quizz.number_questions-1
    id_quizz= question.quizz.id
    quizz.save()
    question.delete()
    if request.method == 'POST':
        return HttpResponseRedirect('/quizzes/' + str(id_quizz)+ '/')
    return HttpResponseRedirect('/quizzes/' + str(id_quizz)+ '/')


#=========when you do questions===========================================
def doing_quizz(request,id_quizz):
    quizz = get_object_or_404(Quizzes,id = id_quizz)
    questions_list = Questions.objects.filter(quizz = quizz)
    students = quizz.in_class.students.all()
    if request.POST:
        leng = len(questions_list)
        mark = leng
        empty = 0
        for Question in questions_list:
            answer = 'Answer'+str(Question.id)
            if request.POST.get(answer) is not None:
                if not str(Question.correct_ans) == str(request.POST.get(answer)):
                    mark = mark - 1
            else :
                empty = empty +1
                mark = mark - 1
        return HttpResponseRedirect('/result/'+str(quizz.id)+'/'+str(request.user)+'/'+str(mark)+'/'+str(empty)+'/')
    return render_to_response('doing_quizzes.html',context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':quizz,'questions_list':questions_list,'list_students':students}))
    
    
#============the return when you completed quizz=================================
def result(request,id_quizz,name_user,val_mark,val_empty):
    quizz = get_object_or_404(Quizzes,id = id_quizz)
    questions_list = Questions.objects.filter(quizz = quizz)
    leng = len(questions_list)
    mark = int(val_mark)
    empty = int(val_empty)
    wrong = leng - mark - empty
    percent = int(((float(int(float(mark)/float(leng)*100)))/100) *100)
    return render_to_response('result.html',context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':quizz,'mark':mark,'leng':leng,'empty':empty,'wrong':wrong,'percent':percent}))


#===========the return when you want to see answer of any class===================
def answer(request,id_quizz):
    quizz = get_object_or_404(Quizzes,id = id_quizz)
    questions_list = Questions.objects.filter(quizz = quizz)
    students = quizz.in_class.students.all()
    return render_to_response('answer.html',context_instance=RequestContext(request,{ 'User': request.user,'Quizzes':quizz,'questions_list':questions_list,'list_students':students}))


