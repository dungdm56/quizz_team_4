from django.contrib import admin
from Class.models import Classes
from Quizz.models import Quizzes
from Quizz.models import Questions

#===============================================================================
#===============================================================================
class QuizzesInline(admin.TabularInline):
    model= Quizzes
    extra= 3
#===============================================================================
class ClassesAdmin(admin.ModelAdmin):
    fieldsets= [('Class name', {'fields': ['class_name']}),
                ('Number Students', {'fields': ['number_students']}),
                ('Teacher',{'fields': ['teacher_name']}),
                ('User created',{'fields': ['user']}),
                ('Time Create',{'fields': ['update_time']}),
                ('Date Create',{'fields': ['update_date']})]
    inlines= [QuizzesInline]
    list_display=('class_name', 'teacher_name','user')
    
class QuizzesAdmin(admin.ModelAdmin):
    fieldsets= [('Class', {'fields': ['in_class']}),
                ('Title', {'fields': ['title']}),
                ('Time limit (minutes)',{'fields': ['time_limit']}),
                ('Time Update',{'fields': ['update_time']}),
                ('Date Create',{'fields': ['update_date']})]
    list_display=('title', 'update_time')
    
class QuestionsAdmin(admin.ModelAdmin):
    fieldsets= [('In Quizzes', {'fields': ['quizz']}),
                ('Question', {'fields': ['ques']}),
                ('Answer 1',{'fields': ['ans1']}),
                ('Answer 2',{'fields': ['ans2']}),
                ('Answer 3',{'fields': ['ans3']}),
                ('Answer 4',{'fields': ['ans4']}),
                ('Answer correct',{'fields': ['correct_ans']})]
    list_display=('ques', 'quizz')
    
# Register your models here.
#===============================================================================
admin.site.register(Classes, ClassesAdmin)
#===============================================================================
admin.site.register(Quizzes,QuizzesAdmin)
#===============================================================================
admin.site.register(Questions, QuestionsAdmin)
#===============================================================================
#admin.site.register(Classes)