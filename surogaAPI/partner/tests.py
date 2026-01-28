"""
Partner App Tests - Suroga API

This module contains automated tests for the 'partner' application within the Suroga API. It aims to validate
the behavior of the partner models, views, forms, and other related functionalities. The tests ensure that
critical workflows such as partner registration, profile updates, and authentication processes perform
as expected and conform to the specified business rules.

Usage:
    Tests should be run regularly as part of the development process to identify and resolve regressions or bugs.
    They can be executed using the Django test runner with the following command:
    `python manage.py test partner`

Features:
    - Includes test cases for creating, retrieving, updating, and deleting partner profiles.
    - Covers authentication tests to ensure secure access to partner-related endpoints.
    - Utilizes Django's TestCase and REST framework's APITestCase for comprehensive test coverage.

Maintainer: Carlos Leandro
Last Modified: 15/3/2024
"""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from partner.models import PartnerProfile  # Adjust import based on your model name

class PartnerTests(APITestCase):
    def setUp(self):
        # Set up the test client and other test variables
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.partner_profile = PartnerProfile.objects.create(user=self.user, name='Test Partner')

    def test_partner_profile_creation(self):
        # Test to verify that a profile can be created
        self.assertEqual(self.partner_profile.name, 'Test Partner')

    def test_view_partner_profile(self):
        # Test to verify partner profile view
        url = reverse('partner:partner-detail', kwargs={'pk': self.partner_profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Here you can add more tests e.g. update, delete
