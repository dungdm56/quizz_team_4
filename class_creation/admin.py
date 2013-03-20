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
    fieldsets= [('Class_name', {'fields': ['Name']}), ('Teacher',{'fields': ['Teacher']}) ]
    inlines= [QuizzesInline]
    list_display=('Name', 'Teacher')
    
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