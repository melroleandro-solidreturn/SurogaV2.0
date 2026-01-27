"""
ASGI config for the SurogaAPI project.

The Asynchronous Server Gateway Interface (ASGI) is a specification for Python web applications to communicate 
with web servers, and it is particularly suited for handling asynchronously rather than the synchronous 
approach taken by WSGI, its predecessor. It provides a standard for building asynchronous web applications 
in Python with frameworks that can handle long-lived connections, such as WebSockets, HTTP/2, and more. 

This module, normally named 'asgi.py', configures the ASGI application for the Django project and 
makes it possible to serve the application via ASGI-compliant web servers. Compared to WSGI, ASGI 
supports asynchronous request processing, which allows for more scalable applications that can 
handle simultaneous connections or long-running operations more efficiently.

The `asgi.py` file exposes the ASGI callable — a function or object instance with a `__call__` method. 
This callable is used by ASGI servers to serve the Django application when deployed. It is analogous to 
the WSGI callable provided in `wsgi.py`, but it is designed for asynchronous applications.

To define the 'application' callable, Django provides an 'asgi' module, and specifically a 
`get_asgi_application()` function, which is imported here and used to create the ASGI application instance.

As with WSGI, the 'os.environ.setdefault' call sets the 'DJANGO_SETTINGS_MODULE' before the application 
is created, to tell Django which settings module should be used.

For additional information on ASGI and how to deploy Django applications with ASGI, see the Django official 
documentation: https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the default environment variable for Django's settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'surogaAPI.settings')

# Create the ASGI application instance to be used by an ASGI server.
application = get_asgi_application()
