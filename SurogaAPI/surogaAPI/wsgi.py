"""
WSGI config for the SurogaAPI project.

The Web Server Gateway Interface (WSGI) is a specification for a universal interface 
between the server and web applications. This module, typically named 'wsgi.py', is used 
by Django's deployment process to interface with web servers, such as Apache or gunicorn, 
which serve the actual web pages in a production environment.

This particular file exposes the WSGI callable — this callable object (a function, method, class, 
or an instance with a `__call__` method) is called by the WSGI server to handle each request. 
In Django, the WSGI callable is an instance of the application class provided by Django's 
core WSGI handler, `get_wsgi_application()`.

The `os.environ.setdefault` line sets the `DJANGO_SETTINGS_MODULE` environment variable, 
which provides the Python import path to your Django project's settings module. 
This is how Django knows which settings to use for the particular instance of the application.

For more detailed information about how this works and how to deploy Django using WSGI, 
visit the official Django documentation:
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

# Import Django's function for fetching the WSGI application.
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'surogaAPI' project.
# This environment variable tells Django which settings to use. If it's not set, Django won't work properly.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'surogaAPI.settings')

# Get the WSGI application callable that Django provides by default.
# It's used as a hook for WSGI-compliant web servers to serve your project.
application = get_wsgi_application()
