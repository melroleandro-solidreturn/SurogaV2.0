"""
Suroga Supplier App Test Suite

This module contains test cases for the 'supplier' app within the Suroga API project. It's
designed to ensure that the app's models, views, forms, and other components are working
as expected. Automated tests help in maintaining code quality and stability as the app changes
over time.

Usage:
    Run the tests from the command line using the `python manage.py test supplier` command.
    This will search for tests in this file and any other test files within the 'supplier' app.

References:
    - Django testing documentation: https://docs.djangoproject.com/en/4.0/topics/testing/
    - Writing and running tests: https://docs.djangoproject.com/en/4.0/topics/testing/overview/

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""

from django.test import TestCase


from django.test import TestCase
from .models import ProfileAgency, ProfileRepresentative, Contract, ContractSection
from django.contrib.auth.models import User
from django.utils import timezone

class ProfileAgencyModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        user = User.objects.create_user(username='testuser', password='12345')
        ProfileAgency.objects.create(user=user, Name='Test Agency', Address='123 Test Street')

    def test_name_label(self):
        agency = ProfileAgency.objects.get(id=1)
        field_label = agency._meta.get_field('Name').verbose_name
        self.assertEqual(field_label, 'Name')

    def test_registration_default(self):
        agency = ProfileAgency.objects.get(id=1)
        self.assertEqual(agency.Registration.date(), timezone.now().date())

class ProfileRepresentativeModelTests(TestCase):
    # Add setUpTestData and test methods for ProfileRepresentative model

    pass  # Placeholder for actual test methods

class ContractModelTests(TestCase):
    # Add setUpTestData and test methods for Contract model

    pass  # Placeholder for actual test methods

class ContractSectionModelTests(TestCase):
    # Add setUpTestData and test methods for ContractSection model

    pass  # Placeholder for actual test methods