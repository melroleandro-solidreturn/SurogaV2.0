
from django.urls import path, include,re_path
from rest_framework import routers, serializers, viewsets
from core.views import time_zoneViewSet , RideDurationViewSet #, ServiceTypeViewSet
#from core.views import PathTypeViewSet, LocalViewSet, CountryViewSet, CurrencyViewSet, LanguageViewSet # TechnologyViewSet,
from core.views import CountryViewSet, CurrencyViewSet, LanguageViewSet # TechnologyViewSet,
from core.views import districtregionViewSet, citymunicipalityViewSet
from core.views import equipmentViewSet, publiceventViewSet, soundViewSet, imageViewSet, localwifiViewSet 
from core.views import eventsViewSet

"""
Suroga API - Core Application URL Configuration

This module defines the URL routing for the Core application within the Suroga API project. Utilizing
Django Rest Framework's routing mechanisms, this configuration maps URL patterns to views for handling
API requests related to core functionalities such as time zones, ride durations, countries, currencies,
languages, and more.

Routes are defined using Django's path and include functions, as well as DRF routers for automatically
generating URLs for view sets. This setup is designed to be scalable and easily maintainable as the
application and its API capabilities continue to grow and evolve.

Each URL pattern corresponds to a specific view set, outlining the way HTTP requests are processed,
and determining the behavior expected for CRUD operations on the associated model instances.

References:
    - Django URL dispatcher documentation: https://docs.djangoproject.com/en/4.0/topics/http/urls/
    - Django Rest Framework routing: https://www.django-rest-framework.org/api-guide/routers/

Note: This file should only be modified if changes to URL patterns are required, ensuring that the
modifications adhere to the existing architectural standards and naming conventions.

Maintainer:  Carlos Leandro
Last Modified: 15/3/2024
"""

# Define the app namespace to allow for reverse-matching of URLs within this 'core' app.
app_name = 'core'

# Set up the Django Rest Framework (DRF) router, which helps generate URL patterns for a ViewSet automatically.
# The DRF routers determine the URL conf based on common naming conventions for common CRUD (Create-Read-Update-Delete) operations.
router = routers.DefaultRouter()

# The router registers multiple view sets with the corresponding URL pattern.
# This allows DRF to auto-generate URLs for accessing the API endpoints,
# typically ones that map closely to database models for CRUD operations.

# Each register call adds a new route to handle requests for listed time zones, durations, countries, currencies, etc. 
router.register(r'time_zones', time_zoneViewSet)
router.register(r'duration', RideDurationViewSet)
router.register(r'country', CountryViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'district_region', districtregionViewSet)
router.register(r'city_municipality', citymunicipalityViewSet)
router.register(r'equipment', equipmentViewSet)
router.register(r'public_event', publiceventViewSet)
router.register(r'sound_requirements', soundViewSet)
router.register(r'image_requirements', imageViewSet)
router.register(r'local_wifi', localwifiViewSet)
router.register(r'events', eventsViewSet)


# urlpatterns is the list of URL patterns recognized by the app.
# Each element in the list associates a route pattern with a view or include for further pattern matching.
urlpatterns = [
    # Includes URL patterns for the 'rides' app within this 'core' app. The namespace 'rides' helps ensure reverse URL matching is unique.
    path('rides/',include('rides.urls', namespace='rides')),
    
    # Include router-generated URL patterns, which will cover the CRUD URLs for all registered view sets.
    # This is a shorthand to include all the URLs handled by the router, allowing DRF to handle the request dispatching.
    path('', include(router.urls)),
]