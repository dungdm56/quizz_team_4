'''
Admin
'''
# pylint: disable-msg=R0904
from django.contrib import admin
from Class.models import Classes
from Quizz.models import Quizzes
from Quizz.models import Questions


#===================================================
class QuizzesInline(admin.TabularInline):
    '''
    Line of Quizz
    '''
    model = Quizzes
    extra = 3
#===================================================


# class manage data in admin page
class ClassesAdmin(admin.ModelAdmin):
    '''
    Admin of Classes
    '''
    fieldsets = [('Class name', {'fields': ['class_name']}),
                ('Number Students', {'fields': ['number_students']}),
                ('Teacher', {'fields': ['teacher_name']}),
                ('User created', {'fields': ['user']}),
                ('Time Create', {'fields': ['update_time']}),
                ('Date Create', {'fields': ['update_date']}),
                ('Lock', {'fields': ['locked']})]
    inlines = [QuizzesInline]
    list_display = ('class_name', 'teacher_name', 'user','locked')


class QuizzesAdmin(admin.ModelAdmin):
    '''
    Admin of Quizzes
    '''
    fieldsets = [('Class', {'fields': ['in_class']}),
                ('Title', {'fields': ['title']}),
                ('Time limit (minutes)', {'fields': ['time_limit']}),
                ('Time Update', {'fields': ['update_time']}),
                ('Date Create', {'fields': ['update_date']})]
    list_display = ('title', 'update_time')


class QuestionsAdmin(admin.ModelAdmin):
    '''
    Admin of Questions
    '''
    fieldsets = [('In Quizzes', {'fields': ['quizz']}),
                ('Question', {'fields': ['ques']}),
                ('Answer 1', {'fields': ['ans1']}),
                ('Answer 2', {'fields': ['ans2']}),
                ('Answer 3', {'fields': ['ans3']}),
                ('Answer 4', {'fields': ['ans4']}),
                ('Answer correct', {'fields': ['correct_ans']})]
    list_display = ('ques', 'quizz')


# Register models
#====================================================
admin.site.register(Classes, ClassesAdmin)
admin.site.register(Quizzes, QuizzesAdmin)
admin.site.register(Questions, QuestionsAdmin)
