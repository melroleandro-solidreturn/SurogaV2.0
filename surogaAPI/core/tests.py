from django.test import TestCase
from django.urls import reverse
from .models import time_zone, Language, Currency, country, citymunicipality
from django.contrib.auth.models import User

"""
Core Application Test Cases - Suroga API

This module contains a suite of test cases for the Core application of the Suroga API project. These tests 
are designed to ensure that the application's models and their methods behave as expected. Unit tests can 
save time and prevent errors by automatically checking for the correct behavior during development and before deployment.

The `TestCase` class from Django's testing framework provides a set of assertions to verify conditions 
and a test database isolated from the production data. Here we include tests for the string representation 
(`__str__`) methods of the models, which are crucial for accurate identification in the Django admin and 
throughout the application.

Usage:
- `setUpTestData`: Used to create objects shared by all test methods. Objects created here use the test database 
  and are cleaned up after all the tests in the `TestCase` class have run.
- `setUp`: Used to set up objects that may be modified by the tests themselves. Each test method will get a fresh 
  copy of these objects.
- Individual test methods: Defined to perform specific assertions.

Examples:
- Ensuring models return their `name` as their string representation.
- Verifying the correctness of model fields and properties.
- Checking the integrity of application logic under various conditions.

Maintainer: Carlos Leandro
Last updated: 15/3/2014

Refer to Django's testing documentation for detailed instructions on writing and running tests:
https://docs.djangoproject.com/en/4.0/topics/testing/
"""

# CoreModelTests is a TestCase class containing a collection of unit tests for the models in the core app.
class CoreModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # This method is called once at the beginning of the test run for setting up class-level test data.
        # Here, it's used to create a test user that can be shared across several different tests.
        cls.test_user = User.objects.create_user('testuser', password='12345')

    def setUp(self):
        # The setUp method is called before every test function to set up any objects that may be modified by the test.
        # If there is no setup necessary beyond what's done in setUpTestData, you can simply pass.
        pass

    def test_str_method_time_zone(self):
        # Ensures the __str__ method of the time_zone model works correctly by returning the time zone's name.
        # Creates a new time_zone instance and compares the result of converting it to a string with the expected name.
        time_zone_obj = time_zone.objects.create(Name='UTC', TimeZone='Universal Time Coordinated', UTCoffset=0)
        self.assertEqual(str(time_zone_obj), time_zone_obj.Name)

    def test_str_method_language(self):
        # Checks the Language model's __str__ method to verify it properly returns the name of the language.
        # It's important that such fundamental methods of models return the correct values for ease of admin interface use and debugging.
        language_obj = Language.objects.create(Name='English', Code='en')
        self.assertEqual(str(language_obj), language_obj.Name)

    def test_str_method_currency(self):
        # Tests the __str__ method of the Currency model to ensure it matches the expected behavior, 
        # which, in this case, is returning the currency's name.
        currency_obj = Currency.objects.create(Name='Euro', Currency='EUR', CurrencySymbol='€', SymbolRight=False)
        self.assertEqual(str(currency_obj), currency_obj.Name)

    def test_str_method_country(self):
        # Validates that the __str__ method for the country model correctly outputs the country's name.
        # Comparing to hardcoded values is suitable for absolute outcomes such as this.
        country_obj = country.objects.create(Name='TestLand', PhoneCode='123')
        self.assertEqual(str(country_obj), country_obj.Name)

    def test_str_method_citymunicipality(self):
        # Assures that the __str__ method for citymunicipality outputs the correct city or municipality name.
        # This test also illustrates how a ForeignKey relationship needs to be set up, creating a needed 'district' instance first.
        district = districtregion.objects.create(Name='TestDistrict')
        city_municipality_obj = citymunicipality.objects.create(Name='TestCity', districtregion=district)
        self.assertEqual(str(city_municipality_obj), city_municipality_obj.Name)

# More tests can be added for each model and view within the core app.