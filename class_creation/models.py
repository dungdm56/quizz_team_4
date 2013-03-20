from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class Classes(models.Model):
    Name= models.CharField(max_length= 200)
    Access_number= models.CharField(max_length=40)
    Teacher= models.CharField(max_length= 60)
    Teacher_email= models.EmailField(max_length=200)
    Permission= models.BooleanField()
        


class Quizzes(models.Model):
    Class= models.ForeignKey(Classes)
    Title= models.CharField(max_length= 200)
    Update_time=  models.TimeField('date published')
    Time_limit= models.IntegerField()
    User_quizze= models.CharField(max_length= 200)



class Questions(models.Model):
    quizz= models.ForeignKey(Quizzes)
    Ques= models.CharField(max_length= 1000)
    Ans1= models.CharField(max_length= 500)
    Ans2= models.CharField(max_length= 500)
    Ans3= models.CharField(max_length= 500)
    Ans4= models.CharField(max_length= 500)
    Correct_ans= models.CharField(max_length= 500)

        
        
    
    
    
        
    