from django.http.request import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve, reverse
from uvaguide.views import map
from django.contrib.auth.models import User 

"""
Testing the login feature
"""
class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='b27', password='password')
        self.client = Client()
        self.login = self.client.login(username='b27', password='password')
        self.response = self.client.get('/')
        self.html = str(self.response.content)

    def test_valid_google_login(self):
        self.assertTrue(self.login, "Login was unsuccessful.")
    
    def test_invalid_google_login(self):
        login = self.client.login(username='b28', password='pass')
        self.assertFalse(login, "Fake login was able to login.")
    
    def test_logged_in_users_can_access_home(self):
        welcome_message = f'Welcome, {self.user.username}!'
        self.assertIn(welcome_message, self.html, "Welcome message does not appear")
    
    def test_not_logged_in_users_redirect_to_login(self):
        self.client.logout()
        html = str(self.client.get('/').content)
        login_message = "Hello, please login."
        self.assertIn(login_message, html, "Login message does not appear.")
    
    def test_fake_users_redirect_to_login(self):
        self.client.logout()
        login = self.client.login(username='b28', password='pass')
        html = str(self.client.get('/').content)
        login_message = "Hello, please login."
        self.assertFalse(login, "Fake login was able to login.")
        self.assertIn(login_message, html, "Login message does not appear.")
        

"""
Testing the maps feature
"""
class MapsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='b27', password='password')
        self.client = Client()
        self.login = self.client.login(username='b27', password='password')
        self.response = self.client.get('/map/lawn/')
        self.html = str(self.response.content)

    def test_valid_maps_response_code(self):
        self.assertEquals(self.response.status_code, 200, 'Maps default page not getting 200 response code')  

    def test_map_page_pulling_from_base_html(self):
        base_footer = 'Authors: CS3240 Group 27'
        self.assertIn(base_footer, self.html, 'Base page not being pulled for map page')

    def test_valid_maps_variable_passing_through(self):
        map = '<iframe id="map" height=90% width=100% style="border:0" loading="lazy" allowfullscreen src=https://www.google.com/maps/embed/v1/place?key=AIzaSyCdaz10ER7OvsL15_iMY2hozh7-KEsukb4&amp;q=lawn,Charlottesville+VA>' 
        self.assertIn(map, self.html, 'Variable not being passed through from url')

class MapsDirectionsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='b27', password='password')
        self.client = Client()
        self.login = self.client.login(username='b27', password='password')
        self.response = self.client.get('/map/lawn/lawn/')
        self.html = str(self.response.content)

    def test_valid_directions_response_code(self):
        self.assertEquals(self.response.status_code, 200, 'Directions default page not getting 200 response code') 

    def test_valid_directions_variable_passing_through(self):
        map = 'src=https://www.google.com/maps/embed/v1/directions?origin=lawn,Charlottesville+VA&amp;destination=lawn,Charlottesville+VA&amp;mode=walking&amp;key=AIzaSyCdaz10ER7OvsL15_iMY2hozh7-KEsukb4' 
        self.assertIn(map, self.html, 'Variable not being passed through from url')
        