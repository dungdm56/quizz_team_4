from django.contrib import admin
from class_creation.models import Classes
from class_creation.models import Quizzes
from class_creation.models import Questions

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
                ('Time Create',{'fields': ['Update_time']}),
                ('Date Create',{'fields': ['Update_date']})]
    inlines= [QuizzesInline]
    list_display=('class_name', 'teacher_name','user')
    
class QuizzesAdmin(admin.ModelAdmin):
    fieldsets= [('Class', {'fields': ['Class']}),
                ('Title', {'fields': ['Title']}),
                ('Time limit (minutes)',{'fields': ['Time_limit']}),
                ('Time Update',{'fields': ['Update_time']}),
                ('Date Create',{'fields': ['Update_date']})]
    list_display=('Title', 'Update_time')
    
class QuestionsAdmin(admin.ModelAdmin):
    fieldsets= [('In Quizzes', {'fields': ['quizz']}),
                ('Question', {'fields': ['Ques']}),
                ('Answer 1',{'fields': ['Ans1']}),
                ('Answer 2',{'fields': ['Ans2']}),
                ('Answer 3',{'fields': ['Ans3']}),
                ('Answer 4',{'fields': ['Ans4']}),
                ('Answer correct',{'fields': ['Correct_ans']})]
    list_display=('Ques', 'quizz')
    
# Register your models here.
#===============================================================================
admin.site.register(Classes, ClassesAdmin)
#===============================================================================
admin.site.register(Quizzes,QuizzesAdmin)
#===============================================================================
admin.site.register(Questions, QuestionsAdmin)
#===============================================================================
#admin.site.register(Classes)