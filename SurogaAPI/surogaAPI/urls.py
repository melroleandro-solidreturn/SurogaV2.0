"""surogaAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from django.contrib.auth import views as auth_views
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from django.conf import settings
from django.conf.urls.static import static

from core import views as coreviews

# urlpatterns define the URL routing for the Suroga API project.
urlpatterns = [
    # Includes URL patterns from the 'partner' app, using a namespace to differentiate these URLs
    # from others that may have the same name in different apps.
    path('partner/',include('partner.urls', namespace='partner')),
    
    # Django's built-in administrative interface. Only intended for use by site administrators.
    path('admin/', admin.site.urls),
    
    # Includes URL patterns from the 'core' app, namespaced for 'core', used for API endpoints.
    path('api/v1/',include('core.urls', namespace='core')),
    
    # URLs for Django REST framework's own login and logout views.
    # These are typically used for browsable API views, which are useful during development.
    path('api-auth/', include('rest_framework.urls')),
    
    # Generates and serves the API documentation page using Django REST framework's documentation feature.
    # These URLs are serialized and presented in an interface for developers to read and understand
    # the capabilities of the API.
    path('docs/', include_docs_urls(
        title="Suroga openapi: Surrogate your rides",
        description="API is used to build bridges between the real and the virtual world.\n Surrogate rides in your APP.",
    )),


    # Serves the generated OpenAPI schema at the `/openapi` endpoint, providing a machine-readable
    # definition of the API that can be used by a variety of tools, such as code generators, documentation
    # generators, and API testing tools. The OpenAPI standard is widely supported and enables interoperability.
    path('openapi', get_schema_view(
        title="Suroga openapi: Surrogate your rides",
        description="API is used to build bridges between the real and the virtual world.\n Surrogate rides in your APP.",
        version="1.0.0"
    ), name='openapi-schema'),
   
    # The root endpoint of the website, which serves the index view from the 'core' app. This view
    # might display a landing page or redirect to a main part of the application.
    path('', coreviews.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)