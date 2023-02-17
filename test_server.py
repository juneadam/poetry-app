# testing
import os
from unittest import TestCase
import unittest
from flask import session
from server import app
import server
from model import connect_to_db, db
from seed_database import seed_database


# ============ Testing simple GET request HTML renders ============ #

class FlaskTestsSimpleRenders(TestCase):
    
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb", echo=False)

        # Create tables and add sample data
        db.create_all()
        seed_database()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_homepage_route(self):
        """Testing HTML render for the homepage"""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Poetry Toolkit</h1>', result.data)

    def test_poems_route(self):
        """Testing HTML render for the poems page."""

        result = self.client.get('/poems')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div class="col-8" id="poem-hole">', result.data)

    def test_prompts_route(self):
        """Testing HTML render for the prompts page."""

        result = self.client.get('/prompts')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Poetry Prompts</h1>', result.data)

    def test_mashups_route(self):
        """Testing the HTML render for the mashups page."""

        result = self.client.get('/mashups')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Mashup Generator!</h1>', result.data)

    def test_add_prompt_route_success(self):
        """Testing the HTML render for the add_prompt page."""

        with self.client.session_transaction() as sess:
        # set a user id without going through the login route
            sess["user_id"] = 1
            sess["username"] = 'userX'

        result = self.client.get('/add-prompt')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<label for="text-box-for-adding-a-new-prompt-to-the-database">', result.data)

    def test_add_prompt_route_failure(self):
        """Testing the HTML render when the log in fails."""

        with self.client:
            result = self.client.get('/add-prompt', follow_redirects=True)
            self.assertEqual(result.status_code, 200, result.data)
            self.assertIn(b'You must be logged in to access this feature.', result.data)



# ============ Testing sign-up POST requests ============ #  

class FlaskTestsSignup(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb", echo=False)

        # Create tables and add sample data
        db.create_all()
        seed_database()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_signup_route_success(self):
        """Testing the sign-up route with a working set of data."""

        with self.client:
            result = self.client.post('/sign-up', data={
                'email': 'new_user@test.com',
                'username': 'new_user',
                'password1': 'new_user_pw',
                'password2': 'new_user_pw'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            self.assertIn(b'Your account was created successfully!', result.data)

    def test_signup_route_unmatched(self):
        """Testing the sign-up route with data including non-matching passwords."""

        with self.client:
            result = self.client.post('/sign-up', data={
                'email': 'new_user@test.com',
                'username': 'new_user',
                'password1': 'new_user_pw',
                'password2': 'new_user_pwzzz'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            self.assertIn(b'Passwords do not match, please try again.', result.data)        
            
    def test_signup_route_preexisting(self):
        """Testing the sign-up route with data including a pre-existing email address."""
        
        with self.client:
            result = self.client.post('/sign-up', data={
                'email': 'test@email.test',
                'username': 'new_user',
                'password1': 'new_user_pw',
                'password2': 'new_user_pw'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            self.assertIn(b'This email is already associated with an account.', result.data)



# ============ Testing login POST requests ============ #

class FlaskTestsLogin(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb", echo=False)

        # Create tables and add sample data
        db.create_all()
        seed_database()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login_route_success(self):
        """Testing the login route with existing data."""

        with self.client:
            result = self.client.post('/login', data={
                'email': 'test@email.test',
                'password': 'test'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            assert session['user_id'] == 1
            self.assertIn(b'You have logged in successfully!', result.data)

    def test_login_route_unmatched(self):
        """Testing the login route with an existing email address and 
        an incorrect password."""

        with self.client:
            result = self.client.post('/login', data={
                'email': 'test@email.test',
                'password': 'testy'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            assert session['user_id'] is None
            self.assertIn(b'Email and password do not match, please try again.', result.data)

    def test_login_route_unknown_user(self):
        """Testing the login route with incorrect data."""

        with self.client:
            result = self.client.post('/login', data={
                'email': 'test@test.test',
                'password': 'testy'
            }, follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            assert session['user_id'] is None
            self.assertIn(b'User not found, please create an account below!', result.data)


# ============ testing logout routes ============ #

class FlaskTestsLogout(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, db_uri="postgresql:///testdb", echo=False)

        # Create tables and add sample data
        db.create_all()
        seed_database()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_logout_success(self):
        """Testing the login route when user data is stored in the session."""

        with self.client.session_transaction() as sess:
        # set a user id without going through the login route
            sess["user_id"] = 1
            sess["username"] = 'userX'

        with self.client:
            result = self.client.get('/logout', follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            self.assertIn(b'You have successfully logged out.', result.data)

    def test_logout_not_logged_in(self):
        """Testing the login route when no user is logged in."""

        with self.client:
            result = self.client.get('/logout', follow_redirects=True)

            self.assertEqual(result.status_code, 200, result.data)
            self.assertIn(b'You must be logged in to access this feature.', result.data)



    # ============ testing poems JSON routes ============ #





if __name__ == "__main__":
    os.system('dropdb testdb')
    os.system('createdb testdb')
    unittest.main()