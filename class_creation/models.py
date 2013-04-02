from django.db import models
from django import forms
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from cProfile import label
from django.template.defaultfilters import default
from django.forms.widgets import Widget
from calendar import timegm
from idlelib.AutoComplete import AutoComplete
from django.conf.locale.sl.formats import TIME_INPUT_FORMATS

# Create your models here.
class Classes(models.Model):
    user = models.ForeignKey(User,db_column = 'user_created_id')
    class_name = models.CharField( max_length= 200)
    number_students = models.IntegerField(default = 0)
    teacher_name = models.CharField(max_length=200)
    Update_time=  models.TimeField('Time published')
    Update_date = models.DateField('Date published')
    
    def __unicode__(self):
        return self.class_name
    
    
class RegistrationClassForm(forms.Form ):
    class_name = forms.CharField(label='Class name', max_length= 200)
    number_students = forms.IntegerField(label='Number students')
    teacher_name = forms.CharField(label='Teacher name',max_length=200)
    
    class Meta:
        model = Classes
                
    def clean_class_name(self):
        class_name = self.cleaned_data['class_name']
        if not class_name :
            raise forms.ValidationError('Enter the name of class !')
        name_exist = Classes.objects.filter(class_name__iexact = class_name)
        if len(name_exist) >=1 :
            raise ValidationError('That name already registerd for different class, choose another one')
        return class_name
    
    def clean_number_students(self):
        number_students = self.cleaned_data['number_students']
        if not number_students:
            raise forms.ValidationError('Enter the number of students')
        if number_students > 50:
            raise forms.ValidationError('The number of students must less than or equal 50')
        return number_students
    
    def clean_teacher_name(self):
        teacher_name = self.cleaned_data['teacher_name']
        if not teacher_name :
            raise forms.ValidationError('Enter the name of teacher!')
        return teacher_name

class Quizzes(models.Model):
    Class= models.ForeignKey(Classes,db_column='in_class')
    Title= models.CharField(max_length= 200)
    Update_time=  models.TimeField('date published')
    Update_date = models.DateField('Date published')
    Time_limit= models.IntegerField()
    
    def __unicode__(self):
        return self.Title
    
class MakeQuizzForm(forms.Form):
    Title = forms.CharField(label = 'Title',max_length=200)
    Time_limit = forms.IntegerField(label = 'Time limit (mins)')
    
    class Meta:
        model = Quizzes
        
    def clean_Title(self):
        title = self.cleaned_data['Title']
        if not title :
            raise forms.ValidationError('Enter the title of Quizzes !')
        title_exist = Quizzes.objects.filter(Title__iexact = title)
        if len(title_exist) >=1 :
            raise ValidationError('That title already maked for different Quizzes, choose another one')
        return title

class Questions(models.Model):
    quizz= models.ForeignKey(Quizzes)
    Ques= models.TextField(max_length= 1000)
    Ans1= models.TextField(max_length= 500)
    Ans2= models.TextField(max_length= 500)
    Ans3= models.TextField(max_length= 500)
    Ans4= models.TextField(max_length= 500)
    Correct_ans= models.TextField(max_length= 500)

class MakeQuestionsForm(forms.Form):
    Ques= forms.CharField(label='Question',max_length= 1000)
    Ans1= forms.CharField(label='Answer 1',max_length= 500)
    Ans2= forms.CharField(label='Answer 2',max_length= 500)
    Ans3= forms.CharField(label='Answer 3',max_length= 500)
    Ans4= forms.CharField(label='Answer 4',max_length= 500)
    Correct_ans= forms.CharField(label='Answer correct',max_length= 500)
        
        
    
    
    
        
    