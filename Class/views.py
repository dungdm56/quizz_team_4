
from django.template import RequestContext

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from Class.models import RegistrationClassForm, Classes, CheckInformationOfClass
from Quizz.models import Quizzes
from django.shortcuts import get_object_or_404
import datetime

# Create your views here.
#=======create new class===============================================
def create_class(request):
    if request.method == 'POST':
        class_form = RegistrationClassForm(request.POST)
		
		#check if the information is valid or not
        if class_form.is_valid():
			#create new Class in Classes model
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
	
	#when teacher want to add new students in this class
    if request.POST.get('add_students') :
        student = User.objects.get(id = request.POST.get('add_students'))
        _class.students.add(student)
        _class.save()
		
	#when teacher want to delete any students in this class
    if request.POST.get('students_delete'):
        list_students = request.POST.getlist('students_delete')
        for name in list_students:
            student = User.objects.get(username = name)
            _class.students.remove(student)
        _class.save()
		
	#get data about students of this class 
    students = _class.students.all()
    length = len(students)
	
    return render_to_response('class.html',context_instance=RequestContext(request,{ 'User': request.user,'Class':_class,'Quizzes_list':quizz,'list_user':list_user,'list_students':students,'length':length}))

	
#=======when you want to edit your class================================
def edit_class(request,id_class):
    _class = get_object_or_404(Classes,id = id_class)
    if request.POST :
		
		#check if the class_name be changed or not
        if not _class.class_name == request.POST.get('class_name'):
            class_form = RegistrationClassForm(request.POST)
        else :
            class_form = CheckInformationOfClass(request.POST)
			
		#check information after edit are valid or not
        if class_form.is_valid():
            _class.user = request.user
            _class.class_name = request.POST.get('class_name')
            _class.number_students = request.POST.get('number_students')
            _class.teacher_name = request.POST.get('teacher_name')
            _class.save()
            return HttpResponseRedirect('/class/'+str(_class.id)+'/')
		
    return render_to_response('edit/edit_class.html',context_instance=RequestContext(request,{ 'User': request.user,'Class':_class}))


