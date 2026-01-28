"""
Rides Application Configuration - Suroga API

This module defines the application configuration for the Rides app within the Suroga API project.
The AppConfig subclass provides metadata and configuration options for the app, such as the default
field type for auto-generated model primary keys and the application label.

Usage:
    The configuration class `RidesConfig` is usually referenced in the project settings in the
    INSTALLED_APPS list to include this application within the project setup.

Best Practices:
    Avoid modifying the 'name' attribute without updating the project settings accordingly.
    Any changes to 'default_auto_field' should be coupled with the appropriate database migrations.

References:
    - Django AppConfig documentation: https://docs.djangoproject.com/en/4.0/ref/applications/#appconfig-classes

Maintainer: Carlos Leandro
Last Modified: 15/3/2024
"""
from django.apps import AppConfig


class RidesConfig(AppConfig):
    """
    The AppConfig subclass defining metadata and default configuration for the Rides application.
    """
    default_auto_field = 'django.db.models.BigAutoField' # Specifies the default AutoField type for primary keys
    name = 'rides' # The full Python path to the application, used by Django for identifying the app
