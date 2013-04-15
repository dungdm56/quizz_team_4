from django.test import TestCase, Client
from django.contrib.auth.models import User
from models import Classes
import datetime
from django.contrib.auth.views import User


class TestView(TestCase):
	def setUp(self):
		self.class_one = Classes.objects.create(
			user = User.objects.create_user( username = 'user1',password = 'pass1',email = 'email1@gmail.com'),
			class_name = 'Devil',
			number_students = 20,
			teacher_name = 'Hung', 
			update_time = datetime.datetime.now(),
			update_date = datetime.datetime.now()
		)
		self.class_one.save()
		
	
	def test_class_create_success(self):
		response = self.client.get('/create_class_success/1/')
		self.assertEqual(response.status_code, 200)
		
	def test_class_list(self):
		response = self.client.get('/class/1/')
		self.assertEqual(response.status_code, 200)
		
	def test_edit_class(self):
		response = self.client.get('/edit_class/1/')
		self.assertEqual(response.status_code, 200)
	
	
	