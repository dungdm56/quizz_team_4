"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from models import *
import unittest

class TestUser(TestCase):
    fixtures = ['accounts_views_testdata.json']
    
    def setUp(self):
        self.user1 = User.objects.create(
            username = 'user1',
            password = 'pass1',
            email = 'email1@gmail.com',
        )
        self.user2 = User.objects.create(
            username = 'user2',
            password = 'pass2',
            email = 'email2@gmail.com',               
        )
        
    def test_home_page(self):
        resp = self.client.get('/home/')
        self.assertEqual(resp.status_code, 200)
        
    def test_form(self):
        
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.id, 1)
        
        self.user2.email = 'email22@gmail.com'
        self.assertEqual(self.user2.email, 'email22@gmail.com')
        self.assertEqual(self.user1.password, 'pass1')
        
        c = Client()
        c.login(username = self.user1.username, password = self.user1.password)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create new account')
        
        response = self.client.post('/register/', {'username': 'abc', 'password' : 'abc', 'email': 'abc@gmail.com'})
        self.assertEqual(response.status_code, 200)
        
        

        
        