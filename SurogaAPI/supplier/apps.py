"""
Suroga Supplier App Configuration

This module contains the Django AppConfig subclass for the 'supplier' app. AppConfig classes
are used by Django to configure application properties and behaviors. This is the class that
represents the supplier application configuration and is used to set up any application-specific
settings such as the default field types for database models.

Django uses this class to get information about the application and especially when initializing
the application during the startup process.

Attributes:
    default_auto_field: Specifies the default AutoField to use as a primary key for models
                        within this application when no field is explicitly specified. Using
                        'BigAutoField' supports a larger number of objects.
    name: The full Python path of the application, used by Django to reference and import
          the app as needed throughout the project.

Tips:
    Make sure to point the 'INSTALLED_APPS' setting in the project's `settings.py` file to
    this AppConfig class to ensure application configuration is correctly applied.

References:
    - AppConfig documentation: https://docs.djangoproject.com/en/4.0/ref/applications/#django.apps.AppConfig
    - Applications in Django: https://docs.djangoproject.com/en/4.0/ref/applications/

Maintainer: Carlos Leandro
Last Modified: 15/4/2014
"""
from django.apps import AppConfig


class SupplierConfig(AppConfig):
    # This property is a string that points to a model field class to be used as the default for primary key fields
    # if no specific primary key field is defined in a model. The 'BigAutoField' is recommended for new projects as it
    # provides a 64-bit integer field that auto-increments. This is generally used when expecting a high number of objects
    # to avoid primary key value exhaustion.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The 'name' property sets a string that defines the full Python path to the app. In this case, the app is named 'supplier'.
    # This dotted path is how Django identifies and imports the app throughout the project. The name is used in various
    # Django commands and settings, such as the INSTALLED_APPS setting in the project's settings.py file which is used to
    # include this app within the project.
    name = 'supplier'
