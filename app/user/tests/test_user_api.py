"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# API url that we will test
CREATE_USER_URL = reverse('user:create')

# Helper function to create a user to be tested


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)

# Separate the tests that require auth and do not


class PublicUserApiTests(TestCase):
    """Test the public features of the API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successfull"""
        # All information to register a new user
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        # Post the data to the API to create a user
        res = self.client.post(CREATE_USER_URL, payload)

        # Check response, creating objects in the db
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Retrieves the object from the db and check it
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        # Make sure the password hash does not return for the user
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        # Create user with the same email as created before
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is return if password less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Check if the user already exists
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
