# create your model here
'''
Created on Feb 28, 2013

'''
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re
email_length = 30
text_length = 60

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length = text_length)
    first_name = forms.CharField(label='First name', max_length = text_length, required=False)
    last_name = forms.CharField(label='Last name', max_length = text_length, required=False)
    email = forms.EmailField(label='Email', max_length = email_length)
    email_confirm = forms.EmailField(label='Email confirmation', max_length= email_length)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Password comfirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username')
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric character and underscore')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('That username already registerd by different user, choose another one')

    # Raise error if two passwords didn't match
    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise ValidationError('Password does not match, please try again')
        return password_confirm

    # Check whether or not an user with existen email have registerd
    def clean_email(self):
        email = self.cleaned_data['email']
        users_exist = User.objects.filter(email__iexact=email)
        if len(users_exist) >= 1:
            raise ValidationError('An username with that email have been existed')
        return email

    # Raise error if two emails didn't match
    def clean_email_confirm(self):
        email = self.cleaned_data.get('email', '')
        email_confirm = self.cleaned_data['email_confirm']
        if email != email_confirm:
            raise ValidationError('Two emails you have entered did not match, try again')
        return email_confirm
    
    

class EditProfileForm(forms.ModelForm):
    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(label='First name', max_length=50, required=False)
    last_name = forms.CharField(label='Last name', max_length=50, required=False)
    email = forms.EmailField(label='Email', max_length=100, required = False)
    new_password = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)
    conf_password = forms.CharField(label='Confirm new password', widget=forms.PasswordInput, required=False)
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.email
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
        except User.DoesNotExist:
            pass

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'new_password', 'conf_password', 'current_password')
        
    def clean_current_password(self):
        cur_pass = self.cleaned_data['current_password']
        if not self.instance.check_password(cur_pass):
            raise ValidationError('You must enter you current password to save change.')
        return cur_pass
    
    def clean_email(self):
        new_email = self.cleaned_data['email']
        email_list = User.objects.filter(email__exact = new_email).exclude(id = self.instance.id)
        if len(email_list) > 0:
            raise ValidationError('This email have used by another user!!!')
        return new_email
    
    def clean_confirm_password(self):
        newPass = self.cleaned_data['new_password']
        confPass = self.cleaned_data['conf_password']
        if (newPass != confPass):
            raise ValidationError('Password does not match, please try again')
        return newPass
        
    def save_data(self):
        user = self.instance
        user.email = self.cleaned_data.get('email', user.email)
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        new_password = self.cleaned_data['new_password']
        if new_password is not None:
            user.set_password(new_password)
        user.save()