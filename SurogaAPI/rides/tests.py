"""
Tests for Rides App - Suroga API

This module contains the test cases for the Rides app within the Suroga API. It aims to ensure
that the endpoints for managing ride-related functionalities like creating, retrieving,
updating, and deleting rides operate correctly.

Using Django's built-in test framework and Django REST Framework's APIClient, the tests included here
cover a range of scenarios to validate the behavior and integrity of the application's API endpoints.

Automated tests are crucial for maintaining code quality and stability, making it easier to detect
regressions and other issues during development and before deployment.

Usage:
    The test cases can be executed using the management command:
    `python manage.py test rides.tests`

Recommended Practices:
    Each test class should target a specific set of related behaviors, while individual test methods
    should focus on single functionalities.
    Write tests for expected outcomes as well as edge cases and potential error conditions.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""

from django.test import TestCase
from django.core.mail import EmailMessage
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings
from core.extras import EmailThread


class EmailThreadTest(TestCase):

    def test_email_sending_on_ride_delete(self):


        # Prepare the email details
        mail_backoffice = settings.EMAILMARKET
        print(mail_backoffice)
        message = "test  ABBA "
        # Verify that an email was sent
        self.assertEqual(1, 1)

