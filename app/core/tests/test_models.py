from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'exmple01@exmplae.com'
        password = 'q2w3e4r5'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for e new user is normalized"""
        email = 'example@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'q2w3e4r5')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'q2w3e4r5')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'example02@example.com',
            'q2w3e4r5'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
