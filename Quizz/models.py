from django.db import models
from django import forms
from django.core.validators import ValidationError
from Class.models import Classes

# Create your models here.
class Quizzes(models.Model):
    in_class = models.ForeignKey(Classes,db_column='in_class')		# Class of this quizz.
    title = models.CharField(max_length= 200)						# Title of this quizz
    update_time=  models.TimeField('date published')
    update_date = models.DateField('Date published')
    time_limit= models.IntegerField()								# Limited time to do this quizz.
    number_questions = models.IntegerField()
    
    def __unicode__(self):
        return self.title

# Create Form of Quizz.    
class MakeQuizzForm(forms.Form):
    title = forms.CharField(label = 'Title',max_length=200)
    time_limit = forms.IntegerField(label = 'Time limit (mins)')
    
    class Meta:
        model = Quizzes
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if not title :													# Check that title is not null.
            raise forms.ValidationError('Enter the title of Quizzes !')	# Return error notification when you didn't enter title.
        title_exist = Quizzes.objects.filter(title__iexact = title)		# Check to make sure that title of class is unique.
        if len(title_exist) >=1 :
            raise ValidationError('That title already maked for different Quizzes, choose another one')		# Return error notification when this title, the same as exist title in database
        return title

# Create Questions models.		
class Questions(models.Model):
    quizz= models.ForeignKey(Quizzes)				# quizz of this question.
    ques= models.TextField(max_length= 1000)		# Question component of question packet.
    ans1= models.CharField(max_length= 500)			# The first answer to choose.
    ans2= models.CharField(max_length= 500)			# The second answer to choose.
    ans3= models.CharField(max_length= 500)			# The third answer to choose.
    ans4= models.CharField(max_length= 500)			# The fourth answer to choose.
    correct_ans= models.IntegerField()				# The index of correct answer.
# Create Question form.
class MakeQuestionsForm(forms.Form):
    ques= forms.CharField(label='Question',max_length= 1000)		# Question component of question packet.
    ans1= forms.CharField(label='answer 1',max_length= 500)			# The first answer to choose.
    ans2= forms.CharField(label='answer 2',max_length= 500)			# The second answer to choose.
    ans3= forms.CharField(label='answer 3',max_length= 500)			# The third answer to choose.
    ans4= forms.CharField(label='answer 4',max_length= 500)			# The fourth answer to choose.
    correct_ans= forms.IntegerField(label='answer correct')			# The index of correct answer.
        
        
    
    
    
        
    