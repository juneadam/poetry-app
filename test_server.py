# testing
import os
from unittest import TestCase
import unittest
from flask import session
from server import app
import server
from model import connect_to_db, db
from seed_database import seed_database

class FlaskTests(TestCase):
    
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        # os.system('dropdb testdb')
        # os.system('createdb testdb')
        connect_to_db(app, db_uri="postgresql:///testdb", echo=False)

        # Create tables and add sample data
        db.create_all()
        seed_database()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    # ============ Testing simple GET request HTML renders ============ #

    def test_homepage_route(self):
        """Testing HTML render for the homepage"""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Poetry Toolkit</h1>', result.data)

    def test_poems_route(self):
        """Testing HTML render for the poems page"""

        result = self.client.get('/poems')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div class="col-8" id="poem-hole">', result.data)

    def test_prompts_route(self):
        """Testing HTML render for the homepage"""

        result = self.client.get('/prompts')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Poetry Prompts</h1>', result.data)


    # ============ Testing POST requests & HTML renders ============ #

    def test_login_route(self):
        """Testing conditions of login route."""

        with self.client:
            result = self.client.post('/login', data={
                'email': 'test@email.test',
                'password': 'test'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            assert session['user_id'] == 1
            self.assertIn(b'You have logged in successfully!', result.data)

        with self.client:
            result = self.client.post('/login', data={
                'email': 'test@email.test',
                'password': 'testy'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            assert session['user_id'] is None
            self.assertIn(b'Email and password do not match, please try again.', result.data)


        with self.client:
            result = self.client.post('/login', data={
                'email': 'test@test.test',
                'password': 'testy'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            assert session['user_id'] is None
            self.assertIn(b'User not found, please create an account below!', result.data)

            

    def test_signup_route(self):

        result = self.client.post('/sign-up', data={
            'email': 'new_user@test.com',
            'username': 'new_user',
            'password1': 'new_user_pw',
            'password2': 'new_user_pw'
        }, follow_redirects=True)

if __name__ == "__main__":
    os.system('dropdb testdb')
    os.system('createdb testdb')
    unittest.main()