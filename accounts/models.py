# create your model here
'''
Created on Feb 28, 2013

'''
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re

#global variable
email_length = 30		#length of email address
text_length = 60		#length of input text for another components

#Form class for register an new account
class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length = text_length)								#the name used to login
    first_name = forms.CharField(label='First name', max_length = text_length, required=False)			#the first name of user
    last_name = forms.CharField(label='Last name', max_length = text_length, required=False)			#the second name of user
    email = forms.EmailField(label='Email', max_length = email_length)									#email of the user
    email_confirm = forms.EmailField(label='Email confirmation', max_length= email_length)				#the email confirm to guarante that the above are extacly
    password = forms.CharField(label='Password', widget=forms.PasswordInput)							#the password to security for account
    password_confirm = forms.CharField(label='Password comfirmation', widget=forms.PasswordInput)		#the password confirm to guarante that the user input correctly password
	
	#the Meta class to define the Model for this form
    class Meta:
        model = User			#this form for User model
    
	#the definition fo checking if the username is valid or not
    def clean_username(self):
        username = self.cleaned_data['username']				#get data from username variable
        if not re.search(r'^\w+$', username):					#check if the username has invalid symbols or not
            raise forms.ValidationError('Username can only contain alphanumeric character and underscore')			#raise error
		
		#check if the username was exist or not
        try:			
            User.objects.get(username=username)					
        except ObjectDoesNotExist:
            return username
			
        raise forms.ValidationError('That username already registerd by different user, choose another one')		#raise error

    # Raise error if two passwords didn't match
    def clean_password_confirm(self):
        password = self.cleaned_data['password']									#get data from password variable
        password_confirm = self.cleaned_data['password_confirm']					#get data from password_confirm variable
        if password != password_confirm:											#check if the password are same the password_confirm or not
            raise ValidationError('Password does not match, please try again')		#raise error
        return password_confirm

    # Check whether or not an user with existen email have registerd
    def clean_email(self):
        email = self.cleaned_data['email']											#get data form email variable
        users_exist = User.objects.filter(email__iexact=email)						#filter all user have same email
		
		#check if the email was exist or not
        if len(users_exist) >= 1:
            raise ValidationError('An username with that email have been existed')	#raise error
        return email

    # Raise error if two emails didn't match
    def clean_email_confirm(self):
        email = self.cleaned_data.get('email', '')									#get data form email variable
        email_confirm = self.cleaned_data['email_confirm']							#get data form email_confirm variable
		
		#check if the email are same the email_confirm or not
        if email != email_confirm:
            raise ValidationError('Two emails you have entered did not match, try again') 	#raise error
        return email_confirm
    
    
#class to edit profile of user
class EditProfileForm(forms.ModelForm):
    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput, required=True)		#the password the user are using
    first_name = forms.CharField(label='First name', max_length=50, required=False)								#the first name of user
    last_name = forms.CharField(label='Last name', max_length=50, required=False)								#the last name of user
    email = forms.EmailField(label='Email', max_length=100, required = False)									#the email of user
    new_password = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)			#the new password of user
    confirm_password = forms.CharField(label='Confirm new password', widget=forms.PasswordInput, required=False)	#the password_confirm for new password
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.email
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
        except User.DoesNotExist:
            pass
	
	#the Meta class to define the Model for this form and order of label  appear
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'new_password', 'confirm_password', 'current_password')
    
	#the definition to check if the current password is correct or not
    def clean_current_password(self):
        cur_pass = self.cleaned_data['current_password']				#get data from current_password variable
		
		#check current password
        if not self.instance.check_password(cur_pass):
            raise ValidationError('You must enter you current password to save change.')		#raise error
        return cur_pass
    
	#the definition to check if the email is valid or not
    def clean_email(self):
        new_email = self.cleaned_data['email']							#get data form email variable
        email_list = User.objects.filter(email__exact = new_email).exclude(id = self.instance.id)	#filter all email that are same new email and exclude old email of this user
		
		#check the email valid
        if len(email_list) > 0:
            raise ValidationError('This email have used by another user!!!')					#raise error
        return new_email
    
	#the definition to check confirm password
    def clean_confirm_password(self):
        new_password = self.cleaned_data['new_password']				#get data form new_password variable
        confirm_password = self.cleaned_data['confirm_password']		#get data from confirm_password variable
		
		#check the passwords are similar
        if (new_password != confirm_password):
            raise ValidationError('Password does not match, please try again')					#raise error
        return new_password
    
	#the definition to save valid data after edition
    def save_data(self):
        user = self.instance													#get user
        user.email = self.cleaned_data.get('email', user.email)					#get email variable of this user 
        user.first_name = self.cleaned_data.get('first_name', user.first_name)	#get first name of this user
        user.last_name = self.cleaned_data.get('last_name', user.last_name)		#get last name of this user
        new_password = self.cleaned_data['new_password']						#get new password variable
		
		#check if the user want change password or not
        if new_password is not None:
            user.set_password(new_password)										#get new password for this user
        user.save()																#save all data for this user