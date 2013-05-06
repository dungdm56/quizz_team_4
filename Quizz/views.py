from django.template import RequestContext
from Class.models import Classes
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import datetime
from Quizz.models import MakeQuizzForm, Quizzes, Questions
from Quiz_Management.views import search


# when you want to create quizzes for your class
def create_quizz(request, id_class):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    classes_list = Classes.objects.filter(user=request.user.id)		# List of class of this user.
    in_class = get_object_or_404(Classes, id=id_class)				# Get class which has id = id_class.

    if request.method == 'POST':
        form = MakeQuizzForm(request.POST)
        # Make sure that form is valid.
        if form.is_valid():
            quizz = Quizzes.objects.create(					# Create new quizz.
                in_class=in_class,							# Set class of new quizz.
                title=form.cleaned_data['title'],			# Get title of quizz from form.
                time_limit=form.cleaned_data['time_limit'],  # Get limited time from form.
                update_time=datetime.datetime.now(),
                update_date=datetime.datetime.now(),		# Get update date of quizz.
                number_questions=0,							# Initial number questions of new quizz is 0.
            )
            quizz.save()

            link = '/class/' + str(quizz.in_class.id) + '/'
            return HttpResponseRedirect(link)
    else:
        form = MakeQuizzForm()
    variables = RequestContext(request, {
        'form': form,
        'User': request.user,
        'classes_list': classes_list
    })
    return render_to_response('creation/quizzes_creation.html', variables)


# When you want to edit quizz

def edit_quizz(request, id_quizz):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    quizz = get_object_or_404(Quizzes, id=id_quizz)		# Get quizz that has id= id_quizz.
    class_of_quizz = quizz.in_class							# Get class of this quizz.

    if request.POST:
        quizz_form = MakeQuizzForm(request.POST)
        # For the situation that no change in title.
        if quizz.title == request.POST.get('title'):
            quizz.time_limit = request.POST.get('time_limit')   # Get update limited time for this quizz.
            quizz.save()										# Save changes of this quizz.

            link = '/quizzes/' + str(quizz.id) + '/'
            return HttpResponseRedirect(link)		# Return to quizz page.

        # For the situation that quizz title is changed.
        if quizz_form.is_valid():
            quizz.title = request.POST.get('title')				# Get update title for this quizz.
            quizz.time_limit = request.POST.get('time_limit')   # Get update limited time for this quizz.
            quizz.save()										# Save changes of this quizz.

            link = '/quizzes/' + str(quizz.id) + '/'
            return HttpResponseRedirect(link) 	# Return to quizz page.

    variables = RequestContext(request, {
        'User': request.user,
        'Quizz': quizz,
        'Classes': class_of_quizz
    })
    return render_to_response('edit/edit_quizz.html', variables)


# the return when you want to visit a quizz page
def quizzes(request, id_quizz):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    quizz = get_object_or_404(Quizzes, id=id_quizz)			# Get quizz from id = id_quizz.
    questions_list = Questions.objects.filter(quizz=quizz)  # List all questions of this quizz.
    students = quizz.in_class.students.all()				# Get all student of class of this quizz.

    variables = RequestContext(request, {
        'User': request.user,
        'Quizzes': quizz,
        'questions_list': questions_list,
        'list_students': students
    })
    return render_to_response('quizzes.html', variables)


# when you want to create questions for your quizzes

def create_question(request, id_quizz):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    state = ' '											# The notification for error enter value.
    quizz = get_object_or_404(Quizzes, id=id_quizz)		# Get quizz from id = id_quizz.
    question = request.POST.get('ques')					# Get question for new Question.
    answer1 = request.POST.get('ans1')
    answer2 = request.POST.get('ans2')
    answer3 = request.POST.get('ans3')
    answer4 = request.POST.get('ans4')
    correct_answer = request.POST.get('correct_ans')

    if request.method == 'POST':
        # Check that all fields are entered.
        if question and answer1 and answer2 and answer3 and answer4 and correct_answer:
            question = Questions.objects.create(		# Create new question.
                quizz=quizz,							# Set quizz of  new question is abobe quizz.
                ques=question,							# Set question for new Question.
                ans1=answer1,							# Set the first answer for new Question.
                ans2=answer2,							# Set the second answer for new Question.
                ans3=answer3,							# Set the third answer for new Question.
                ans4=answer4,							# Set the fourth answer for new Question.
                correct_ans=correct_answer				# Set the index correct answer for new Question.
                )
            question.save()											# Save new Question.
            quizz.number_questions = quizz.number_questions + 1		# Increase number of question of quizz of new question.
            quizz.save()										    # Save change of quizz.

            link = '/quizzes/' + str(question.quizz.id) + '/'
            return HttpResponseRedirect(link)			# Return to quizz page.
        else:
            state = 'Please enter all information'		# Return error if some fields is missed.

    variables = RequestContext(request, {
        'User': request.user,
        'Quizzes': quizz
    })
    return render_to_response('creation/questions_creation.html', {'state': state}, variables)


# When you want to edit question

def edit_question(request, id_question):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    question = get_object_or_404(Questions, id=id_question)
    state = ' '
    in_quizz = question.quizz
    ques = request.POST.get('ques')
    answer1 = request.POST.get('ans1')
    answer2 = request.POST.get('ans2')
    answer3 = request.POST.get('ans3')
    answer4 = request.POST.get('ans4')
    correct_ans = request.POST.get('correct_ans')

    if request.method == 'POST':
        # Check that all update fields are entered.
        if ques and answer1 and answer2 and answer3 and answer4 and correct_ans:
                quizz = in_quizz			# Set quizz of  new question is abobe quizz.
                question.ques = ques		# Set update question for this Question.
                question.ans1 = answer1		# Set the first answer for this Question.
                question.ans2 = answer2		# Set the second answer for this Question.
                question.ans3 = answer3		# Set the third answer for this Question.
                question.ans4 = answer4		# Set the fourth answer for this Question.
                question.correct_ans = correct_ans		# Set update index correct answer for this Question.
                question.save()		# Save changes of question.
                quizz.save()		# Save changes of quizz.

                link = '/quizzes/' + str(question.quizz.id) + '/'
                return HttpResponseRedirect(link)
        else:
            state = 'Please enter all information'		# Return error notification if some fields is missed.
    variables = RequestContext(request, {
        'User': request.user,
        'Quizz': in_quizz,
        'Question': question,
        'state': state
    })
    return render_to_response('edit/edit_question.html', variables)


# When you want to delete question

def delete_question(request, id_question):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    question = get_object_or_404(Questions, id=id_question)		# Get question from id= id_question.
    quizz = question.quizz										# Get quizz of this question.
    quizz.number_questions = quizz.number_questions - 1			# Decrease number questions of quizz of this question.
    id_quizz = question.quizz.id
    quizz.save()												# Save change of quizz.
    question.delete()											# Delete this question.

    link = '/quizzes/' + str(id_quizz) + '/'
    return HttpResponseRedirect(link)


#when you do questions

def doing_quizz(request, id_quizz):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    quizz = get_object_or_404(Quizzes, id=id_quizz)			# Get quizz from id= id_quizz.
    questions_list = Questions.objects.filter(quizz=quizz)  # List all questions of this quizz.
    students = quizz.in_class.students.all()				# List all students of class of this quizz.

    if request.POST:
        #make some variable to calculate result
        leng = len(questions_list)			# the number of question
        mark = leng							# the mark after finish
        empty = 0							# the number of empty question after finish

        #calculate result
        for Question in questions_list:
            answer = 'Answer' + str(Question.id)

            #check if the question have answer or not
            if request.POST.get(answer) is not None:
                if not str(Question.correct_ans) == str(request.POST.get(answer)):
                    mark = mark - 1
            else:
                empty = empty + 1
                mark = mark - 1
        link = '/result/' + str(quizz.id) + '/' + str(request.user) + '/' + str(mark) + '/' + str(empty) + '/'
        return HttpResponseRedirect(link)

    variables = RequestContext(request, {
        'User': request.user,
        'Quizzes': quizz,
        'questions_list': questions_list,
        'list_students': students
    })
    return render_to_response('doing_quizzes.html', variables)


# the return when you completed quizz

def result(request, id_quizz, name_user, val_mark, val_empty):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    #some variable for context in web page
    quizz = get_object_or_404(Quizzes, id=id_quizz)
    questions_list = Questions.objects.filter(quizz=quizz)  # get all questions of this quizz
    leng = len(questions_list)								# get number of questions
    mark = int(val_mark)									# get mark for test
    empty = int(val_empty)									# get empty question students have not done
    wrong = leng - mark - empty								# get the number of wrong answer
    percent = int(((float(int(float(mark) / float(leng) * 100))) / 100) * 100)		# get the percent of correct answer

    variables = RequestContext(request, {
        'User': request.user,
        'Quizzes': quizz,
        'mark': mark,
        'leng': leng,
        'empty': empty,
        'wrong': wrong,
        'percent': percent
    })
    return render_to_response('result.html', variables)


# the return when you want to see answer of any class

def answer(request, id_quizz):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    #some variable for context in web page
    quizz = get_object_or_404(Quizzes, id=id_quizz)
    questions_list = Questions.objects.filter(quizz=quizz)  # get all questions of this quizz
    students = quizz.in_class.students.all()				# get all students in this class

    variables = RequestContext(request, {
        'User': request.user,
        'Quizzes': quizz,
        'questions_list': questions_list,
        'list_students': students
    })
    return render_to_response('answer.html', variables)
