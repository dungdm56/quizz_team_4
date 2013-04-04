from django.test import TestCase, Client

from django.contrib.auth.models import User
from class_creation.models import Classes
from django.contrib.auth.models import User
from accounts.models import *
from django.template.defaultfilters import time
from django.utils.datetime_safe import datetime
 

class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'admin',
            password = 'admin',
            email = 'admin@gmail.com',
        )
        self._class = Classes.objects.create(
            user = self.user,
            class_name = 'k56-ca',
            number_students = 50,
            teacher_name = 'FinalDevil',
            Update_time = datetime.now(),
            Update_date = datetime.now(),
        )
        self._class.save()
        self.client = Client()
    
    def test_create_class_success(self):
        response = self.client.get('/class_creation_success/')
        self.assertEqual(response.status_code, 200)