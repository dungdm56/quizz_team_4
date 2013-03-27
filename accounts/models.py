#create your model here
'''
Created on Feb 28, 2013

'''
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 30)
    full_name = forms.CharField(label = 'Full name', max_length = 60)
    email1 = forms.EmailField(label = 'Email', max_length = 30)
    email2 = forms.EmailField(label = 'Email confirmation', max_length = 30)
    password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Password comfirmation', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username')
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric character and underscore')
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('That username already registerd by different user, choose another one')

    # Raise error if two passwords didn't match
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Password does not match, please try again')
        return password2

    # Check whether or not an user with existen email have registerd
    def clean_email1(self):
        email1 = self.cleaned_data['email1']
        users_exist = User.objects.filter(email__iexact = email1)
        if len(users_exist) >= 1:
            raise ValidationError('An username with that email have been existed')
        return email1

    # Raise error if two emails didn't match
    def clean_email2(self):
        email1 = self.cleaned_data.get('email1','')
        email2 = self.cleaned_data['email2']
        if email1 != email2:
            raise ValidationError('Two emails you have entered did not match, try again')
        return email2
    
