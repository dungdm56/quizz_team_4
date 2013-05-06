'''
models.py
'''
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


#====Classes model=========================================
class Classes(models.Model):
    '''
    Model Classes
    '''
    objects = models.Manager()
    user = models.ForeignKey(User, \
        db_column='user_created_id', related_name='user')
    class_name = models.CharField(max_length=200)     #Name of class
    number_students = models.IntegerField(default=0)  #Number of students
    teacher_name = models.CharField(max_length=200)   #Teacher of class
    update_time = models.TimeField('Time published')  #Time of the last update
    update_date = models.DateField('Date published')  #Date of the last update
    students = models.ManyToManyField(User)  # Contain all students
    locked = models.BooleanField(default = False)

    def __unicode__(self):  # Show as title of this class
        return self.class_name


# RegistrationClassForm model to make and check form for class model
class RegistrationClassForm(forms.Form):
    '''
    Registration class form
    '''
    # All form in Registation class
    class_name = forms.CharField(label='Class name', max_length=200)
    number_students = forms.IntegerField(label='Number students')
    teacher_name = forms.CharField(label='Teacher name', max_length=200)


    # class Meta to show that the form get variables for model class
    class Meta:
        '''
        Meta class
        '''
        def __init__(self):
            pass
        # Definition the Form get data for model Classes
        model = Classes

    # Some common method
    def __len__(self, key):
        pass

    def __setitem__(self, name, item):
        pass

    def __delitem__(self, name):
        pass

    # function to check if the class_name in model Classes valid or not
    def clean_class_name(self):
        '''
        check class_name variable
        '''
        # Get class name entered by user
        class_name = self.cleaned_data['class_name']
        # Check class name is empty or not
        if not class_name:
            raise forms.ValidationError('Enter the name of class !')
        name_exist = Classes.objects.filter(class_name__iexact=class_name)
        # Check if the class name are like different class or not
        if len(name_exist) >= 1:
            raise ValidationError(\
                'That name already registerd for different class,\
                choose another one')
        return class_name

    # function to check if the number_students in model Classes valid or not
    def clean_number_students(self):
        '''
        check number students
        '''
        # Get number students from form
        number_students = self.cleaned_data['number_students']
        # Check if the number students is empty or not
        if not number_students:
            raise forms.ValidationError('Enter the number of students')
        # The number of student must NOT is negative integer and greater than 50
        if number_students > 50 or number_students <= 0:
            raise forms.ValidationError(\
                'The number of students must between 1 and 50')
        return number_students

    # function to check if the teacher_name in model Classes valid or not
    def clean_teacher_name(self):
        '''
        check teacher name
        '''
        teacher_name = self.cleaned_data['teacher_name']
        # It means teacher_name field is empty
        if not teacher_name:
            raise forms.ValidationError('Enter the name of teacher!')
        return teacher_name


# Check infor when user want edit infor of class but not change class_name
class EditClassInformationForm(forms.Form):
    '''
    edit class infor form
    '''
    # All form in Edit class form
    number_students = forms.IntegerField(label='Number students')
    teacher_name = forms.CharField(label='Teacher name', max_length=200)


    # class Meta to show that the form get variables for model class
    class Meta:
        '''
        class Meta
        '''
        def __init__(self):
            pass
        # Definition the Form get data for model Classes
        model = Classes

    # Some common method
    def __len__(self, key):
        pass

    def __setitem__(self, name, item):
        pass

    def __delitem__(self, name):
        pass

    # function to check if the number_students in model Classes valid or not
    def clean_number_students(self):
        '''
        check number students
        '''
        # Get number students from form
        number_students = self.cleaned_data['number_students']
        # Check if the number students is empty or not
        if not number_students:
            raise forms.ValidationError('Enter the number of students')
        # The number of student must NOT is negative integer and greater than 50
        if number_students > 50 or number_students <= 0:
            raise forms.ValidationError(\
                'The number of students must between 1 and 50')
        return number_students

    # function to check if the teacher_name in model Classes valid or not
    def clean_teacher_name(self):
        '''
        check teacher name
        '''
        teacher_name = self.cleaned_data['teacher_name']
        # It means teacher_name field is empty
        if not teacher_name:
            raise forms.ValidationError('Enter the name of teacher!')
        return teacher_name
