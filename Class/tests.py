from django.test import TestCase
from django.contrib.auth.models import User
from models import Classes
import datetime


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
	
	#Test data from database with expected result
	def test_teacher_name(self):
		self.teacher_name = self.class_one.teacher_name
		self.assertEqual(self.teacher_name, 'Hung')
		
	def test_number_students(self):
		self.students = self.class_one.number_students
		self.assertEqual(self.students, 20)
		
	def test_username(self):
		self.user_name = self.class_one.user.username
		self.assertEqual(self.user_name, 'user1')
		
	def test_class_name(self):
		self.class_name = self.class_one.class_name
		self.assertEqual(self.class_name, 'Devil')
	
	#Test if a class is create successfully
	def test_class_create_success(self):
		response = self.client.get('/create_class_success/1/')
		self.assertEqual(response.status_code, 200)
		
	#Test list of classes
	def test_class_list(self):
		response = self.client.get('/class/1/')
		self.assertEqual(response.status_code, 200)
	
	#Test if we can edit a class
	def test_edit_class(self):
		response = self.client.get('/edit_class/1/')
		self.assertEqual(response.status_code, 200)
	
	
	