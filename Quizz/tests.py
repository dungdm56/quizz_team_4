"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from models import Quizzes
from Class.models import Classes
import datetime

class TestVies(TestCase):
	def setUp(self):
		self.quizz = Quizzes.objects.create(
            in_class = Classes.objects.create(
				user = User.objects.create_user( username = 'user1',password = 'pass1',email = 'email1@gmail.com'),
				class_name = 'Devil',
				number_students = 20,
				teacher_name = 'Hung', 
				update_time = datetime.datetime.now(),
				update_date = datetime.datetime.now(),
			),
            title = 'Final',
            time_limit = 20,
            update_time = datetime.datetime.now(),
            update_date = datetime.datetime.now(),
            number_questions = 5,
        )
		self.quizz.save()
	
	def test_class_name(self):
		self.class_name = self.quizz.in_class.class_name
		self.assertEqual(self.class_name, 'Devil')
	
	def test_teacher_name(self):
		self.teacher_name = self.quizz.in_class.teacher_name
		self.assertEqual('Hung', self.teacher_name)
	
	def test_time_limit(self):
		self.time = self.quizz.time_limit
		self.assertEqual(20, self.time)
	
	def test_number_question(self):
		number = self.quizz.number_questions
		self.assertEqual(5, number)
		
		
		
		
		