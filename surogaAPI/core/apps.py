from django.apps import AppConfig

"""
Core Application Configuration - Suroga API

This module contains the application configuration for the 'core' app within the Suroga API Django project. It is used by 
Django's application registry to configure app-specific settings such as the name of the app and the default auto field 
type for the database models.

In larger projects with multiple apps, each app would have a similar configuration class, typically found in its 
'apps.py' module, to hold its unique settings and metadata. This configuration is critical for Django to properly 
handle different applications and make features such as models and signals available to the rest of the project.

The CoreConfig class extends Django's AppConfig and customizes the behavior of the 'core' app. By setting attributes 
like 'default_auto_field' we ensure that any auto-created primary key fields use a big integer field, which is 
necessary for databases that will store a large number of records.

Maintainer: Carlos Leandro
Last updated: 15/3/2024

Refer to Django's documentation for more details on application configurations:
https://docs.djangoproject.com/en/4.0/ref/applications/
"""

# The CoreConfig class is used by Django's app configuration system to hold
# metadata for the 'core' application. It defines common application properties
# and acts as a container for app-specific configurations.

class CoreConfig(AppConfig):
    # Specifies the default field type for auto-generated primary key fields.
    # The 'BigAutoField' is a 64-bit integer, generally useful if you anticipate
    # that your data will exceed the maximum auto-increment value of standard AutoFields.
    default_auto_field = 'django.db.models.BigAutoField'

    # The 'name' attribute defines the full Python path to the application.
    # Django uses this attribute to identify the app and its configuration.
    name = 'core'
