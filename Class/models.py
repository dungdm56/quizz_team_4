from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

#====Classes model=========================================
class Classes(models.Model):
    user = models.ForeignKey(User,db_column = 'user_created_id',related_name = '+')
    class_name = models.CharField( max_length= 200)
    number_students = models.IntegerField(default = 0)
    teacher_name = models.CharField(max_length=200)
    update_time=  models.TimeField('Time published')
    update_date = models.DateField('Date published')
    students = models.ManyToManyField(User)
    
    def __unicode__(self):
        return self.class_name
    
#====RegistrationClassForm model to make and check form for class model
class RegistrationClassForm(forms.Form ):
    class_name = forms.CharField(label='Class name', max_length= 200)
    number_students = forms.IntegerField(label='Number students')
    teacher_name = forms.CharField(label='Teacher name',max_length=200)
    
    # class Meta to show that the form get variables for model class
    class Meta:
        model = Classes
		
    # function to check if the class_name in model Classes valid or not
    def clean_class_name(self):
        class_name = self.cleaned_data['class_name']
        if not class_name :
            raise forms.ValidationError('Enter the name of class !')
        name_exist = Classes.objects.filter(class_name__iexact = class_name)
        if len(name_exist) >=1 :
            raise ValidationError('That name already registerd for different class, choose another one')
        return class_name
    
	# function to check if the number_students in model Classes valid or not
    def clean_number_students(self):
        number_students = self.cleaned_data['number_students']
        if not number_students:
            raise forms.ValidationError('Enter the number of students')
        if number_students > 50 or number_students <= 0:
            raise forms.ValidationError('The number of students must between 1 and 50')
        return number_students
    
	# function to check if the teacher_name in model Classes valid or not
    def clean_teacher_name(self):
        teacher_name = self.cleaned_data['teacher_name']
        if not teacher_name :
            raise forms.ValidationError('Enter the name of teacher!')
        return teacher_name


#Class to check information when user want edit information of class but not change class_name
class CheckInformationOfClass(forms.Form ):
    number_students = forms.IntegerField(label='Number students')
    teacher_name = forms.CharField(label='Teacher name',max_length=200)
    
	# class Meta to show that the form get variables for model class
    class Meta:
        model = Classes
    
	# function to check if the number_students in model Classes valid or not
    def clean_number_students(self):
        number_students = self.cleaned_data['number_students']
        if not number_students:
            raise forms.ValidationError('Enter the number of students')
        if number_students > 50:
            raise forms.ValidationError('The number of students must less than or equal 50')
        return number_students
    
	# function to check if the teacher_name in model Classes valid or not
    def clean_teacher_name(self):
        teacher_name = self.cleaned_data['teacher_name']
        if not teacher_name :
            raise forms.ValidationError('Enter the name of teacher!')
        return teacher_name
