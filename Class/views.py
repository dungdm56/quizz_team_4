'''
view.py
'''
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from Class.models import RegistrationClassForm, \
    Classes, EditClassInformationForm
from Quizz.models import Quizzes
from django.shortcuts import get_object_or_404
import datetime
from Quiz_Management.views import search


# Create your views here.
def create_class(request):
    '''
    Create new class
    '''
    #method for searching
    if request.GET.has_key('search'):
        return search(request)
    if request.method == 'POST':
        class_form = RegistrationClassForm(request.POST)
        # check if the information is valid or not
        if class_form.is_valid():
            # create new Class in Classes model
            new_class = Classes.objects.create(
                user=request.user,
                class_name=class_form.cleaned_data['class_name'],
                number_students=class_form.cleaned_data['number_students'],
                teacher_name=class_form.cleaned_data['teacher_name'],
                update_time=datetime.datetime.now(),
                update_date=datetime.datetime.now()
            )
            # Save new class
            new_class.save()
            link = '/create_class_success/' + str(new_class.id) + '/'
            return HttpResponseRedirect(link)
    else:
        class_form = RegistrationClassForm()
    variables = RequestContext(request, {
        'class_form': class_form,
        'User': request.user
    })
    return render_to_response('creation/class_creation.html', variables)


#=======when you create new class successful============================
def create_class_success(request,  id_class):
    '''
    Create class success
    '''
    #method for searching
    if request.GET.has_key('search'):
        return search(request)
    _class = get_object_or_404(Classes,  id=id_class)
    variables = RequestContext(request, {
        'User': request.user,
        'Class': _class
    })
    return render_to_response('creation/class_creation_success.html', variables)


#=======the return when you visit any class=============================
def classes(request, id_class):
    '''
    class in view
    '''
    _class = get_object_or_404(Classes,  id=id_class)
    quizz = Quizzes.objects.filter(in_class=_class)
    list_user = User.objects.exclude(username=request.user.username)
    # lock and unlock class
    if request.POST.get('unlock_class'):
        _class.locked = False
    if request.POST.get('lock_class'):
        _class.locked = True
    _class.save()
    #method for searching
    if request.GET.has_key('search'):
        return search(request)
    # when teacher want to add new students in this class
    if request.POST.get('add_students'):
        student = User.objects.get(id=request.POST.get('add_students'))
        _class.students.add(student)
        _class.save()
    # when teacher want to delete any students in this class
    if request.POST.get('students_delete'):
        list_students = request.POST.getlist('students_delete')
        for name in list_students:
            student = User.objects.get(username=name)
            _class.students.remove(student)
        _class.save()
    # get data about students of this class
    students = _class.students.all()
    length = len(students)
    variables = RequestContext(request, {
        'User': request.user,
        'Class': _class,
        'Quizzes_list': quizz,
        'list_user': list_user,
        'list_students': students,
        'length': length
    })
    return render_to_response('class.html', variables)


#=======when you want to edit your class================================
def edit_class(request, id_class):
    '''
    edit class
    '''
    _class = get_object_or_404(Classes, id=id_class)
    state = ''

    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    if request.POST:
        # check if the class_name be changed or not
        if not _class.class_name == request.POST.get('class_name'):
            class_form = RegistrationClassForm(request.POST)
        else:
            class_form = EditClassInformationForm(request.POST)
        # check information after edit are valid or not
        if class_form.is_valid():
            number_students = int(request.POST.get('number_students'))
            if number_students >= _class.students.all().count():
                _class.user = request.user
                _class.class_name = request.POST.get('class_name')
                _class.number_students = request.POST.get('number_students')
                _class.teacher_name = request.POST.get('teacher_name')
                _class.save()
                link = '/class/' + str(_class.id) + '/'
                return HttpResponseRedirect(link)
            else:
                state = 'The number of students in class \
                    at the moment is larger than the number you enter'
    
    variables = RequestContext(request, {
        'User': request.user,
        'Class': _class,
        'state': state
    })
    return render_to_response('edit/edit_class.html', variables)
