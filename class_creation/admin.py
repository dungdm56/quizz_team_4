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
                ('User created',{'fields': ['user']})]
    inlines= [QuizzesInline]
    list_display=('class_name', 'teacher_name')
    
    #===========================================================================
    # list_display=('name', 'Teacher')
    #===========================================================================
#===============================================================================

# Register your models here.
#===============================================================================
admin.site.register(Classes, ClassesAdmin)
#===============================================================================
admin.site.register(Quizzes)
#===============================================================================
#===============================================================================
#admin.site.register(Classes)