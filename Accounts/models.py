# create your model here
'''
Created on Feb 28, 2013
'''
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re

# global variable
email_length = 50
text_length = 60

class RegistrationForm(forms.ModelForm):
    """
    Made registration form to register account
    """
    username = forms.CharField(
        label='Username', max_length = text_length)  
    first_name = forms.CharField(
        label='First name', max_length = text_length, required = False)
    last_name = forms.CharField(
        label='Last name', max_length = text_length, required = False)
    email = forms.EmailField(
        label='Email', max_length = email_length)
    email_confirm = forms.EmailField(
        label='Email confirmation', max_length = email_length)
    password = forms.CharField(
        label='Password', widget = forms.PasswordInput)
    password_confirm = forms.CharField(
        label='Password comfirmation', widget = forms.PasswordInput)

    # The Meta class to define the Model for this form
    class Meta:
        """
        Meta class
        """
        def __init__(self):
            pass
        model = User  # this form for User model
        fields = ('username', 'email', 'email_confirm',
            'password', 'password_confirm', 'first_name', 'last_name')

    def clean_username(self):
        """
        Check username
        """
        # get data from username variable
        username = self.cleaned_data['username']
        # check if the username has invalid symbols or not
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(
                'Username can only contain alphanumeric'
                ' character and underscore')
        # check if the username was exist or not
        try:			
            User.objects.get(username=username)					
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError(
            'That username already registerd by' 
             ' different user, choose another one')

    def clean_password_confirm(self):
        """
        Raise error if two passwords didn't match
        """
        # get data from password variable
        password = self.cleaned_data['password']
        # get data from password_confirm variable
        password_confirm = self.cleaned_data['password_confirm']
        # check if the password are same the password_confirm or not
        if password != password_confirm:
            raise ValidationError('Password does not match, please try again')
        return password_confirm

    def clean_email(self):
        """
        Check whether or not an user with existen email have registerd
        """
        email = self.cleaned_data['email']
        users_exist = User.objects.filter(email__iexact=email)
        # check if the email was exist by other user or not
        if len(users_exist) >= 1:
            raise ValidationError(
                'An username with that email have been existed')
        return email

    def clean_email_confirm(self):
        """
        Raise error if two emails didn't match
        """
        email = self.cleaned_data.get('email', '')
        email_confirm = self.cleaned_data['email_confirm']
        # check if the email are same the email_confirm or not
        if email != email_confirm:
            raise ValidationError(
                'Two emails you have entered did not match, try again')
        return email_confirm


class EditProfileForm(forms.ModelForm):
    """
    edit profile of user
    """
    current_password = forms.CharField(
        label='Current password', widget=forms.PasswordInput, required=True)
    first_name = forms.CharField(
        label='First name', max_length=50, required=False)
    last_name = forms.CharField(
        label='Last name', max_length=50, required=False)
    email = forms.EmailField(
        label='Email', max_length=100, required=False)
    new_password = forms.CharField(
        label='New password', widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.email
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
        except User.DoesNotExist:
            pass

    class Meta:
        """
        Meta class 
        """
        model = User
        # Show order of file when it display
        fields = ('first_name', 'last_name', 'email', 
                  'new_password', 'confirm_password', 'current_password')


    def clean_current_password(self):
        """
        check if the current password is correct or not
        """
        cur_pass = self.cleaned_data['current_password']
        # check current password
        if not self.instance.check_password(cur_pass):
            raise ValidationError(
                'You must enter you current password to save change.')
        return cur_pass
 
    def clean_email(self):
        """
        check if the email is valid or not
        """
        new_email = self.cleaned_data['email']
        # emails that are same new email and exclude old email of this user
        email_list = User.objects.filter(email__exact=new_email).exclude(id=self.instance.id)
        # check the validation of your given email
        if len(email_list) > 0:
            raise ValidationError('This email have used by another user!!!')
        return new_email

    def clean_confirm_password(self):
        """
        check confirm password
        """
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']
        # check password and password confirm is match
        if (new_password != confirm_password):
            raise ValidationError('Password does not match, please try again')
        return new_password

    def save_data(self):
        """
        save valid data after edition
        """
        user = self.instance  # get user
        user.email = self.cleaned_data.get('email', user.email) 
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        new_password = self.cleaned_data['new_password']
        # check if the user want change password or not
        if new_password is not None:
            user.set_password(new_password)
        user.save()
