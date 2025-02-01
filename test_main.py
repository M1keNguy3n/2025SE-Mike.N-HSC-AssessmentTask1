import unittest
from flask import Flask
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
import userManagement as dbHandler
from main import app

class TestRegistration(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_database.db"
    TESTING = True

    def create_app(self):
        app.config.from_object(self)
        return app


    def test_register_success(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                email='test@example.com',
                password='password123',
                confirm_password='password123'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Registration successful! You can now log in.', response.data)

    def test_register_existing_user(self):
        dbHandler.insert_users('test@example.com', generate_password_hash('password123'))
        with self.client:
            response = self.client.post('/register', data=dict(
                email='test@example.com',
                password='password123',
                confirm_password='password123'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Email already registered. Please log in.', response.data)

    def test_register_password_mismatch(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                email='test2@example.com',
                password='password123',
                confirm_password='password456'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Passwords do not match. Please try again.', response.data)

if __name__ == '__main__':
    unittest.main()