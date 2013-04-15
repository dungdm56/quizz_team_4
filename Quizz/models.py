from django.db import models
from django import forms
from django.core.validators import ValidationError
from Class.models import Classes

# Create your models here.
class Quizzes(models.Model):
    in_class = models.ForeignKey(Classes,db_column='in_class')
    title = models.CharField(max_length= 200)
    update_time=  models.TimeField('date published')
    update_date = models.DateField('Date published')
    time_limit= models.IntegerField()
    number_questions = models.IntegerField()
    
    def __unicode__(self):
        return self.title
    
class MakeQuizzForm(forms.Form):
    title = forms.CharField(label = 'Title',max_length=200)
    time_limit = forms.IntegerField(label = 'Time limit (mins)')
    
    class Meta:
        model = Quizzes
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if not title :
            raise forms.ValidationError('Enter the title of Quizzes !')
        title_exist = Quizzes.objects.filter(title__iexact = title)
        if len(title_exist) >=1 :
            raise ValidationError('That title already maked for different Quizzes, choose another one')
        return title

class Questions(models.Model):
    quizz= models.ForeignKey(Quizzes)
    ques= models.TextField(max_length= 1000)
    ans1= models.CharField(max_length= 500)
    ans2= models.CharField(max_length= 500)
    ans3= models.CharField(max_length= 500)
    ans4= models.CharField(max_length= 500)
    correct_ans= models.IntegerField()

class MakeQuestionsForm(forms.Form):
    ques= forms.CharField(label='Question',max_length= 1000)
    ans1= forms.CharField(label='answer 1',max_length= 500)
    ans2= forms.CharField(label='answer 2',max_length= 500)
    ans3= forms.CharField(label='answer 3',max_length= 500)
    ans4= forms.CharField(label='answer 4',max_length= 500)
    correct_ans= forms.IntegerField(label='answer correct')
        
        
    
    
    
        
    