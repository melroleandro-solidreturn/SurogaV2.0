"""
Partner Application Configuration - Suroga API

This module defines the default application configuration ['PartnerConfig'] for the Partner app within the Suroga API project.
It specifies application-specific settings, such as the primary key field type for models and the application's name.

The AppConfig class within this file acts as a container for the application's configuration. When Django starts up, it uses
the information contained here to set up aspects of the application, and it can be a place to perform initialization tasks.

Attributes:
    default_auto_field: Specifies the type of auto field to use as a primary key (e.g., BigAutoField for larger number space).
    name: Declares the application namespace and label. This full dotted Python path is used by Django to find and use the app.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014

Example:
    The default_auto_field is recommended to be set to 'BigAutoField' in new Django projects
    to avoid potential issues after a substantial number of objects have been created.
"""
from django.apps import AppConfig


class PartnerConfig(AppConfig):
    """
    Application configuration for the Partner app within the Suroga API project.
    
    This class configures app-specific settings and acts as a hook for performing initialization and configuration tasks
    like setting the default field type for auto-generated primary keys across all models in the 'partner' app.
    
    Attributes:
        default_auto_field: Specifies the default field type to use for auto-generated primary key fields.
                        Django recommends using 'BigAutoField' for new projects to provide more space for the identifiers.
        name: Declares the application's label for internal reference. It is used by Django to tie together
              the application's various components.
    """
    # Specifies the default field type for auto-generated primary key fields.
    default_auto_field = 'django.db.models.BigAutoField'
    # Sets the label for the application in Django's app registry. Important for relating models, views, etc., to the correct app.
    name = 'partner'
