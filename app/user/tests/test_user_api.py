from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test create user with valid payload is successful"""
        payload = {
            'email': 'test10@test.com',
            'password': 'testpass',
            'name': 'Test api'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists"""
        payload = {
            'email': 'test10@test.com',
            'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 chars"""
        payload = {
            'email': 'test10@test.com',
            'password': 'pwd'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for the user"""
        payload = {
            'email': 'test10@gmail.com',
            'password': 'testpass',
            'name': 'Test'
        }
        create_user(**payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        print(user_exists)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials"""
        create_user(email='test100@gmail.com', password='wrong')
        payload = {
            'email': 'test10@test.com',
            'password': 'password1123'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exists"""
        payload = {
            'email': 'test10@test.com',
            'password': 'password123'
        }
        res = self.client.post(TOKEN_URL,  payload)
        self.assertNotIn('token',  res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missed_fields(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'qq', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)