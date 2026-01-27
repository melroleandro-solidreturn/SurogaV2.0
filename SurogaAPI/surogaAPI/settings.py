"""
Django Settings Configuration for the SurogaAPI Project

This file contains a comprehensive list of settings that configure the core behavior of the SurogaAPI Django
application. Settings cover everything from database connections, internationalization preferences,
middleware components, static file handling, security precautions, to custom application variables.

Remark: The configurations herein are tailored for both development and production environments.
Special attention should be given to securing sensitive information such as secret keys, database credentials,
and third-party API tokens. It's advisable to utilize environment variables or dedicated secrets management
tools for production deployments.

Reference Documentation:
- Django settings: https://docs.djangoproject.com/en/4.0/topics/settings/
- Deployment checklist: https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR is a reference to the root directory of the Django project. It is used to construct paths 
# throughout the rest of the settings file in a platform-independent way.

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# The following lines provide instructions and warnings about settings that are specific to a development 
# environment and should be changed or secured when deploying to a production environment.

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY is a critical setting that should be kept secret and unique to each Django project. It's used for cryptographic signing and should never be checked into version control in production.
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG is a boolean that turns on/off debug mode. Never deploy a site into production with DEBUG turned on.
DEBUG = True

# ALLOWED_HOSTS defines a list of host/domain names that this site can serve. This is a security measure 
# to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations.
#ALLOWED_HOSTS = ['127.0.0.1','suroga-api.azurewebsites.net','localhost']
ALLOWED_HOSTS = ['127.0.0.1','api.greenconnections.eu','localhost']

# Application definition
# INSTALLED_APPS is a list of strings designating all applications that are enabled in this Django project. 
# These are used to include various configurations and features from the apps to the project.
INSTALLED_APPS = [
    # Default Django apps that provide the base authentication system, session management,
    # messaging framework, and static assets handling.
    'django.contrib.auth',  # User authentication system
    'django.contrib.contenttypes',  # Framework for content types used by Django's permission system
    'django.contrib.sessions',  # Session framework for managing user sessions
    'django.contrib.messages',  # Messaging framework for displaying temporary messages to the user
    'django.contrib.staticfiles', # Managing static files (CSS, JavaScript, Images)
    
    # Third-party app 'widget_tweaks' allows for easy manipulation of form rendering in templates.
    'widget_tweaks',

    # Custom apps created for the Suroga API project; these contain the business logic and data models.
    'core', # May handle core functionality that's common across the application
    'supplier', # Manages suppliers on the platform
    'kit',  # Manages kits, could be related to equipment or packages needed for rides
    'partner', # Manages partner entities or accounts on the platform
    'rides',# Handles the logic and data models for booking and managing rides

    # Django Rest Framework (DRF) apps that provide tools to build web APIs.
    'rest_framework', # Core framework for building RESTful APIs in Django
    'django.contrib.admin',  # These configuration settings include Django’s built-in admin application
    'rest_framework.authtoken', # Token-based authentication for APIs in Django

    # Django Rest Framework API logger app for tracking requests to the API and logging them.
    'drf_api_logger',  # Captures and logs API requests and responses
]

# MIDDLEWARE is a list of middleware to use during request/response processing.
# Order is important and may affect behavior.
MIDDLEWARE = [
    # Adds security features to the HTTP responses. A key middleware that's crucial for safe web operations.
    'django.middleware.security.SecurityMiddleware', 
    
    # Manages sessions across requests, crucial for keeping a persisting state (e.g., login sessions) across the browser visits.
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # WhiteNoise allows Django to serve static files efficiently, especially suitable for production use.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    # Handles some common tasks — it can block User-Agents and set Content-Length, among other things.
    'django.middleware.common.CommonMiddleware',
    
    # Provides protection against Cross-Site Request Forgeries, which is crucial for security.
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Associates users with requests using sessions. This is essential for handling user logins.
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Handles temporary messages (flash messages) transfer between views.
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Adds protection against clickjacking. Prevents render of your pages in an iframe.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # The 'drf_api_logger' middleware captures all the requested endpoint requests and responses.
    # It is useful for debugging and logging API usage.
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',  #API loger
]

# Root URL configuration
# ROOT_URLCONF points to the Python module that contains the root URL patterns for the project.
ROOT_URLCONF = 'surogaAPI.urls'

# Login URLs
# LOGIN_REDIRECT_URL is the path to redirect to after successful login when no 'next' parameter is present.
LOGIN_REDIRECT_URL = '/partner/confirmLogin'

# LOGIN_URL is the path to redirect to for login, typically the path to a login view.
LOGIN_URL = 'login'

# Uncomment the following line if a custom user model is used instead of Django's built-in User model.
# AUTH_USER_MODEL = 'core.User'

# TEMPLATES configures the engine and directory for Django templates.
TEMPLATES = [
    {
        # 'BACKEND' specifies which template engine to use. Here, Django's built-in template engine is used.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # 'DIRS' is a list of filesystem directories to check when loading templates. It's a way to tell Django where 
        # it should look for template files before it checks the app-specific template directories.
        # BASE_DIR / 'templates' defines a common folder at the root of the project for non-app-specific templates.
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        
        # 'APP_DIRS' when set to True, allows the template engine to look for templates inside installed applications.
        # Each Django application can have its own 'templates' directory which Django will check.
        'APP_DIRS': True,
        
        # 'OPTIONS' provides a collections of custom settings for the template engine.
        # Context processors add variables or information to the context that is passed to every template:
        'OPTIONS': {
            'context_processors': [
                # Adds debug context variables if DEBUG is True.
                'django.template.context_processors.debug',
                
                # Adds 'request' to the context – enabling access to the current HttpRequest in templates.
                'django.template.context_processors.request',
                
                # Adds the 'user' and 'perms' context variables, enabling access to the current user and permissions.
                'django.contrib.auth.context_processors.auth',
                
                # Adds the 'messages' context variable, enabling access to user messages (from Django's messaging framework).
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION refers to the Python path of the WSGI application that Django's built-in server will use.
WSGI_APPLICATION = 'surogaAPI.wsgi.application'

# Internationalization
# Langauges configuration for Django. These are the languages this Django project will support.
LANGUAGES = (
    ('en', 'English'),
    ('pt', 'Português'),
)

# MODELTRANSLATION_DEFAULT_LANGUAGE sets the default language to be used with Django's model translation package.
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

# Database Configuration
# DATABASES is a dictionary that configures the database(s) to be used with Django.
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # Option that was previously used or can be used for connecting g66Jv55TejpJNVA
    # to a Microsoft SQL Server (mssql) database hosted on Azure (as can be deduced from the HOST value). Important
    # details such as HOST, NAME, USER, and PASSWORD would need to be adjusted for actual deployment. However, this 
    # information, particularly the password, should never be committed to version control for security reasons.
    
    #'default': {
    #    'ENGINE': 'mssql',
    #    'HOST': 'tcp:surogasql.database.windows.net',
    #    'NAME': 'surogasql',
    #    'USER':'sqladmin',
    #    'PASSWORD':'gMRd}f^EAp9X*sL',
    #    'PORT': '1433',
    #    'OPTIONS': {
    #        'driver': 'ODBC Driver 17 for SQL Server',
    #        'extra_params':'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    #    }
        
    #}
    
    #For local development or small-scale deployments, the project is set up to use SQLite - this is represented 
    #by the 'default' engine setting.
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password Validators
# AUTH_PASSWORD_VALIDATORS is a list of validators that are used to check the strength of user passwords.

AUTH_PASSWORD_VALIDATORS = [
    {
        # Checks the similarity between the password and a set of attributes of the user.
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # This validator helps prevent users from using passwords that are too similar to their personal information,
        # making it harder for attackers to guess passwords based on user data like username or email.
    },
    {
        # Ensures that a password meets a minimum length, which is a common security requirement.
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # You can set the `OPTIONS` for this validator to specify the `min_length` attribute (default is 8 characters).
        # Longer passwords typically enhance security by making them harder to crack.
    },
    {
        # Checks whether a password is not a common password.
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # This validator uses a list of the most common passwords, which must not be used by users.
        # It is important in preventing the use of passwords which are commonly used and hence are likely to be guessed.
    },
    {
        # Validates whether a password is not entirely numeric.
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Numeric-only passwords are typically easier to guess or crack, so this enforces more complexity.
    },
    # These validators are used when creating a new user or changing passwords. It is important to configure them according
    # to the security policies and requirements of your project. By default, Django enforces these validators to encourage
    # good security practices, but they can be adjusted or extended by creating and adding custom validators if needed.
]

# Django REST Framework Configuration
# REST_FRAMEWORK is a dictionary that configures the behavior of Django REST framework, which provides tools
# for building Web APIs.
REST_FRAMEWORK = {
    # DEFAULT_PERMISSION_CLASSES defines the permissions to apply by default to all views. In this configuration,
    # DjangoModelPermissionsOrAnonReadOnly allows read-only access to unauthenticated users, but other operations
    # like create/update/delete require authentication and the appropriate model permissions.
    
    # DEFAULT_SCHEMA_CLASS sets the class to use for generating API schemas.
    
    # DEFAULT_AUTHENTICATION_CLASSES specifies the authentication methods the API will use. 
    # TokenAuthentication is enabled, which means clients will have to include a valid token in the headers of their 
    # requests to perform authenticated API operations.
    
    # DATE_INPUT_FORMATS defines acceptable date input formats that can be used to parse dates in serializers.
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  
    ],
    'DATE_INPUT_FORMATS': ['iso-8601', '%Y-%m-%dT%H:%M:%S.%fZ'],
}

# API Logger Configuration
# DRF_API_LOGGER configuration determines how API requests and responses are logged when using Django REST framework.

# DRF_API_LOGGER_SKIP_URL_NAME specifies a list of URL names to exclude from logging.
DRF_API_LOGGER_SKIP_URL_NAME = ['events']

# DRF_API_LOGGER_DATABASE is a boolean indicating whether to save API logs to the database.
DRF_API_LOGGER_DATABASE = True

# DRF_API_LOGGER_EXCLUDE_KEYS is a list of sensitive keys whose values should be excluded from the API logs.
DRF_API_LOGGER_EXCLUDE_KEYS = ['password', 'token', 'access', 'refresh']

# DRF_API_LOGGER_METHODS is a list of HTTP methods to include in the logging.
DRF_API_LOGGER_METHODS = ['GET', 'POST', 'DELETE', 'PUT'] 

# DRF_API_LOGGER_STATUS_CODES is a list of HTTP status codes to include in the logging.
DRF_API_LOGGER_STATUS_CODES = ['200', '400', '404', '500'] 

# DRF_LOGGER_QUEUE_MAX_SIZE specifies the max size of the queue for batching log entries before saving to database.
DRF_LOGGER_QUEUE_MAX_SIZE = 50 # Originally set to 50, but reduced for this example.


# Internationalization and Localization
# Configuration of internationalization (i18n), date formats, and time zones.

# DATETIME_FORMAT specifies the string format for datetime objects throughout the project.
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

# LANGUAGE_CODE sets the default language for the project (US English).
LANGUAGE_CODE = 'en-us'

# TIME_ZONE configures the time zone for the project.
TIME_ZONE = 'UTC'

# USE_I18N is a boolean that enables Django's translation system (i18n).
USE_I18N = True

# USE_TZ is a boolean that enables timezone support.
USE_TZ = True

# Email Configuration
# Settings to configure the email backend, including SMTP server details and credentials.

# EMAIL_BACKEND specifies Django’s email backend to use.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


#O365_MAIL_CLIENT_ID = config('O365_MAIL_CLIENT_ID')
#365_MAIL_CLIENT_SECRET = config('O365_MAIL_CLIENT_SECRET')
#O365_MAIL_TENANT_ID = config('O365_MAIL_TENANT_ID')
#O365_ACTUALLY_SEND_IN_DEBUG = True

WEBRTC_URL_BOOKING=config('WEBRTC_URL_BOOKING')
WEBRTC_KEY=config('WEBRTC_KEY')

# settings.py
CONTABO_SMTP_HOST = config('CONTABO_SMTP_HOST')  # Ou IP do seu servidor
CONTABO_SMTP_PORT = config('CONTABO_SMTP_PORT')  # 587 (TLS) ou 465 (SSL)
CONTABO_SMTP_USER = config('CONTABO_SMTP_USER')  # Mailbox real
CONTABO_SMTP_PASSWORD = config('CONTABO_SMTP_PASSWORD')  # Senha da mailbox
CONTABO_SMTP_USE_TLS = True  # Usar para porta 587
CONTABO_SMTP_USE_SSL = False  # Usar para porta 465

# Static Files Configuration
# Specifies URL and directories for handling static files such as CSS, JavaScript, and images.

# STATIC_URL is the URL to use when referring to static files.
STATIC_URL = '/static/'

# STATICFILES_DIRS specifies a list of filesystem directories to check when loading static files.
#azure: 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Other Settings
# Various other Django settings follow, possibly related to specific deployment scenarios (e.g., Azure),
# default field types for database models, API trust settings, etc. Some are commented out and prefaced with 
# 'azure:' indicating they might be used in a specific deployment context (e.g., Azure).


#azure: 
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

#azure: 
#CSRF_TRUSTED_ORIGINS = ['https://suroga-api.azurewebsites.net','https://suroga-api.azurewebsites.net']
CSRF_TRUSTED_ORIGINS = ['https://api.greenconnections.eu','https://api.greenconnections.eu']

# Default primary key field type # test
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

#azure: 
#DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#azure: 
#APPEND_SLASH = True

# Miscellaneous
# Additional placeholders and variables used elsewhere in the project.
#IP_PLACEHOLDER = "2001:8a0:6a14:6900:325a:3aff:fe00:9000"

EMAILMARKET = config('EMAILMARKET')
DOMAIN = config('DOMAIN')

# curl -X POST https://webrtcapi.solid-ai.net/book-room/ -H "Authorization: Token f7018f6a8cf038054c7f9dc2a5987333117e8765" -H "Content-Type: application/json" -d '{"room": 77606, "start_time": "2024-10-15T14:00:00Z", "end_time": "2024-10-15T15:00:00Z"}'