"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User

class TestUser(TestCase):
    """
    Create and run test
    """
    #  fixtures = ['accounts_views_testdata.json']
    def setUp(self):
        self.user1 = User.objects.create_user(
            username = 'user1',
            password = 'pass1',
            email = 'email1@gmail.com',
        )
        self.user2 = User.objects.create_user(
            username = 'user2',
            password = 'pass2',
            email = 'email2@gmail.com',               
        )
        self.user1.save()
        self.user2.save()

    def test_form(self):
        """
        Test artribute
        """
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.id, 1)
        self.assertEqual(self.user2.id, 2)
        self.user2.email = 'email22@gmail.com'
        self.assertEqual(self.user2.email, 'email22@gmail.com')

class TestViews(TestCase):
    """
    Test for views.py
    """
    #  fixtures = ['accounts_views_testdata.json']
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'admin',
            password = 'admin',
            email = 'admin@gmail.com',
        )
        self.user.save()
        self.client = Client()

    def test_home_page(self):
        """
        Tes home page
        """
        resp = self.client.get('/home/')
        self.assertEqual(resp.status_code, 200)

    def test_signup(self):
        """
        Test if a user is register successfully
        """
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create new account')
        self.assertContains(response, 'Password comfirmation')
        response = self.client.post('/register/',
            {'username': 'abc', 'password' : 'abc', 'email': 'abc@gmail.com'})
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        """
        Test whether or not a user is logged successfully
        """
        is_logged_in = self.client.login(username = 'admin', password = 'admin')
        self.assertEqual(is_logged_in, True)

    def test_logout(self):
        """
        Test if a user is logout successfully
        """
        self.client.login(username = 'admin', password = 'admin')
        is_logged_out = self.client.logout()
        self.assertEqual(is_logged_out, None)

    def test_about_page(self):
        """
        Test page
        """
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_signup_success(self):
        """
        Test status of a success user
        """
        response = self.client.get('/signup_success/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'failure', 0)
        self.assertContains(response, 'Successfully', 1)
