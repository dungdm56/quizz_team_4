'''
Created on Mar 22, 2013

@author: NVDAI
'''
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from Class.models import Classes
from Quizz.models import Quizzes
from django.contrib.auth.models import User
from django.db.models import Q


@csrf_protect
# the definition for home method
def home(request):
    #method for searching
    if request.GET.has_key('search'):
        return search(request)

    # check if the user is valid or not
    if request.user is not None:
        # get some variable for context in web page
        classes_list = Classes.objects.filter(user=request.user.id)
        classes_list_joined = Classes.objects.filter(students=request.user.id)
        classes_list_another = Classes.objects.all()
        # return home.html and some context
        return render_to_response('home.html', context_instance=RequestContext(request, {'User': request.user, 'classes_list': classes_list, 'classes_list_another': classes_list_another, 'classes_list_joined': classes_list_joined}))
    else:
        return render_to_response('home.html', context_instance=RequestContext(request, {'User': request.user}))  # return home.html and some context


def search(request):
    query = request.GET['search'].strip()
    show_result = False
    if query:
        show_result = True
        keywords = query.split()
        q = Q()

        for keyword in keywords:
            q_user = q & Q(username__icontains=keyword)
            q_class = q & Q(class_name__icontains=keyword)
            q_quizz = q & Q(title__icontains=keyword)

        user_search = User.objects.filter(q_user)[:10]
        class_search = Classes.objects.filter(q_class)[:10]
        quizz_search = Quizzes.objects.filter(q_quizz)[:10]
        return render_to_response('search_page.html', context_instance=RequestContext(request, {'User': request.user, 'show_result': show_result, 'query': query, 'class_search': class_search, 'quizz_search': quizz_search, 'user_search': user_search}))
    else:
        return render_to_response('search_page.html', context_instance=RequestContext(request, {'User': request.user, 'show_result': show_result}))
