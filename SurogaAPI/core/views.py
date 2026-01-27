
from datetime import datetime, timedelta

from django.shortcuts import render

from rest_framework import routers, serializers, viewsets, generics

from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from django.utils.translation import activate, gettext

from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model
User = get_user_model()

from core.models import events, time_zone, RideDuration
from core.models import  Language, Currency, country
from core.models import  districtregion, citymunicipality  
from core.models import equipment, publicevent, sound, image, localwifi 
from core.serializers import time_zoneSerializer, RideDurationSerializer
from core.serializers import CountrySerializer, LanguageSerializer, CurrencySerializer
from core.serializers import districtregionSerializer, citymunicipalitySerializer  
from core.serializers import equipmentSerializer,publiceventSerializer, soundSerializer, imageSerializer, localwifiSerializer   
from core.serializers import eventsSerializer

from core.models import usertype,userprofile
from partner.models import profilepartner

from drf_api_logger.models import APILogsModel

"""
Core Application Views - Suroga API

This file contains the view logic for the Core application of the Suroga API project. The views are responsible for processing incoming requests and returning appropriate responses. They handle the API endpoints related to essential services and data models, such as equipment, public events, sound requirements, image standards, and Wi-Fi conditions, as well as user events and logs for administrative purposes.

The views in this file utilize Django Rest Framework's ViewSets to provide a convenient interface for representing data models over a RESTful API. The ViewSets are configured with specific permissions to ensure that only authorized users can access or modify the resources as intended by the business logic.

The ViewSets are also configured with appropriate serializers to represent data models as JSON, making it accessible for client applications and ensuring a consistent structure across the API.

Maintainer: Carlos Leandro
Last Modified: 15/3/2024

Please refer to Django and Django Rest Framework documentation for additional details:
- Django Views: https://docs.djangoproject.com/en/4.0/topics/http/views/
- Django Rest Framework ViewSets: https://www.django-rest-framework.org/api-guide/viewsets/
"""

# The index view is the default view for the Suroga API project. It serves the homepage
# and handles redirection based on the user's authentication status and roles.
def index(request, *args, **kwargs):

    # Determine if the current user is anonymous (not logged in).
    is_anonymous = request.user.is_anonymous

    # Initialize a flag for client status. We are assuming this might relate to user types,
    # with is_client indicating a non-admin, authenticated user.
    is_client = False

    # Try to retrieve the language code from the user's session. Fallback to 'en' if not found.
    try:
        code = request.session['code']
    except KeyError:
        code = "en"

    # Activate the selected language for this session or request based on 'code'.
    activate(code)

    # Prepare the context data for the template. Convert 'is_anonymous' to int for template use.
    data = {'is_anonymous': int(is_anonymous),'is_client': 0}

    # If the user is authenticated, further determine their status and redirect accordingly.
    if not is_anonymous:

        is_superuser = request.user.is_superuser
        if is_superuser: # If user is an admin, redirect to the admin dashboard.
            return redirect('/admin/')
        else: # If user is not an admin, treat as a client and redirect to the partner app.
            data['is_client'] = 1
            return redirect('/partner/')

    # If the user is anonymous, render the 'index.html' template with the provided data.
    return render(request, 'index.html', data)


# Custom permission class that implements read-only access.
# It allows unauthenticated users to view the data but not modify it.
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Only allow methods that are deemed "safe" (i.e., read-only) like GET, OPTIONS, and HEAD.
        return request.method in SAFE_METHODS

# time_zoneViewSet defines the view behavior for time zones within the API.
# It extends the ModelViewSet, offering an interface for listing and retrieving time zone instances.
class time_zoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows time zones to be viewed.
    * Requires token authentication.
    * Only authenticated users are given access, with read-only permissions.
    """
    # Define the authentication and permission classes required to access this view.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]

    # Define the queryset that the view will use to retrieve Time Zone objects.
    queryset = time_zone.objects.all()

    # Specify the serializer that should be used to format the Time Zone objects for return to the client.
    serializer_class = time_zoneSerializer

# Similarly, RideDurationViewSet defines the view behavior for ride durations.
class RideDurationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ride durations to be viewed.
    * Requires token authentication.
    * Only authenticated users are given access, with read-only permissions.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = RideDuration.objects.all()
    serializer_class = RideDurationSerializer

# LanguageViewSet extends Django REST Framework's ModelViewSet to provide a full set of views (list, create, retrieve, update, delete)
# for Language objects. The API endpoint will allow clients to view the available languages offered for rides.
class LanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing available languages.

    The `TokenAuthentication` ensures that each request has a valid token, providing user authentication.
    The `ReadOnly` permission allows only read operations (GET requests) for any authenticated user, ensuring
    no changes can be made through this viewset.

    'queryset' collects all instances of the Language model, and the 'serializer_class' formats these instances 
    as JSON responses conforming to the LanguageSerializer fields.
    """ 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

# CurrencyViewSet provides a full set of views for Currency objects, similar to LanguageViewSet,
# allowing clients to view the different types of currency available for transactions within the service.
class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing available currencies.

    This will include the PK, Name of the currency, Currency code, Symbol, and whether the
    Symbol is positioned to the right of currency values.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

# CountryViewSet allows clients to view the service's available countries, providing details
# such as the country's name, currency, language, phone code, time zone, VAT details, GPS coordinates, 
# the zoom level used on maps, and a Google Maps-compatible code.
class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing available countries.

    The retrieved fields include a primary key (pk), Name, Currency, Language, PhoneCode, TimeZone,
    Value-Added Tax (VAT), GPS coordinates, and a ZoomLevel that might be used for map displays along with a Google-specific code.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = country.objects.all()
    serializer_class = CountrySerializer
 

# districtregionViewSet provides views for district or region objects that the service covers,
# It helps users to view various geographic and administrative regions within countries.
class districtregionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing available districts or regions.

    The focus is on geographical regions that are covered by the service, with the response including
    details such as GPS coordinates, zoom levels for maps, and a code compatible with Google's geo APIs.
    
    Retrieve: ['pk','Name','GPS_latitude','GPS_longitude','ZoomLevel','GoogleCode']

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = districtregion.objects.all()
    serializer_class = districtregionSerializer

# citymunicipalityViewSet extends the ModelViewSet for city and municipality objects.
# It offers detailed views of these localities, which are subdivisions of the district/regions.
class citymunicipalityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing available cities and municipalities.

    This ViewSet is scoped to more granular geographical data that includes names, associated
    district or region data (foreign key), plus GPS coordinates, zoom level, and a Google code.
    
    Retrieve: ['pk','Name','districtregion','GPS_latitude','GPS_longitude','ZoomLevel','GoogleCode']

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = citymunicipality.objects.all()
    serializer_class = citymunicipalitySerializer

# equipmentViewSet provides a full set of views for equipment objects. It allows clients to retrieve
# information about the available equipment which might be necessary for the rides or associated services.
class equipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing available equipment.

    The view restricts changes by only providing read-only access to authenticated users, as indicated by
    the `ReadOnly` permission. The queryset contains all equipment objects, formatable by equipmentSerializer.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = equipment.objects.all()
    serializer_class = equipmentSerializer

# publiceventViewSet extends ModelViewSet to provide views for public event objects,
# which might include events where rides are commonly required or provided.

class publiceventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing a list of public event conditions.

    The data returned may include information such as district/region, GPS coordinates, and Google location codes,
    which can be useful for mapping services or event location identification.
    
    Retrieve: ['pk','Name','districtregion','GPS_latitude','GPS_longitude','ZoomLevel','GoogleCode']

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = publicevent.objects.all()
    serializer_class = publiceventSerializer

# soundViewSet allows clients to view possible sound requirements for rides or events,
# which can be essential when planning for events or services that involve audio setup.

class soundViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing a list of sound requirements.

    The endpoint might be used to present different categories or types of sound equipment or services provided.
    

    Retrieve: ['pk','Name']

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = sound.objects.all()
    serializer_class = soundSerializer

# imageViewSet provides views for image requirements, which might be used to specify
# particular photography or image standards for rides or events.

class imageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing a list of image requirements.

    Useful for detailing the image standards or photography guidelines for services offered by Suroga API.
    

    Retrieve: ['pk','Name']

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = image.objects.all()
    serializer_class = imageSerializer

# localwifiViewSet allows clients to view the possible conditions or standards for local wifi services,
# which might be relevant in rides or venues where internet connectivity is a consideration.

class localwifiViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing a list of local wifi conditions.

    Details returned may include technical specifications for wifi services provided or available.
    
    Retrieve: ['pk','Name']

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ReadOnly]
    queryset = localwifi.objects.all()
    serializer_class = localwifiSerializer

# eventsViewSet provides models and tools to view a log of user events.
# It appears to offer logged data related to API usage and user interactions.

class eventsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing user events, which could entail user actions, API call logs, system events, etc.

    The queryset is filtered by the requesting user, ensuring that users can only access their own event logs.
    The commented section suggests filtering of event logs by date range, which is currently not active.
    

    Retrieve: ['pk','Type','Registration','Request']

    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = APILogsModel.objects.all()
    serializer_class = eventsSerializer


    def get_queryset(self):
        # Overrides the standard queryset to return only those API logs that belong to the currently authenticated user.      
        queryset = APILogsModel.objects.filter(user=self.request.user)
        '''
        end   = datetime.today()
        start = end - timedelta(days=8)
    
        startdate = start.strftime("%Y-%m-%d")

        startstr = self.request.query_params.get('Start')
        endstr = self.request.query_params.get('End')

        if startstr is not None:
            None
        elif endstr is not None:
            None
        else:
            queryset = queryset.filter(added_on__gte=start)
        '''
        return queryset
