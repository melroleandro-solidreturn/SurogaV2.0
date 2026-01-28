import datetime
import hashlib
import json
import requests
import ipaddress

from django.dispatch import receiver
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings as conf_settings

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

User = get_user_model()

"""
Core Application Models - Suroga API

This module defines the data models related to the core functionality of the Suroga API. These models serve as the
blueprint for creating the database schema and define the structure of the database records for various entities such as
local Wi-Fi configurations, endpoint versions for API management, communication channels for CRM and support, and more.

The classes included here are utilized throughout the application, where database interactions are required. Each class
corresponds to a table in the database and each attribute of a class is a field in the table.

- localwifi: Provides data around various Wi-Fi configurations offered by local venues or the service itself.
- version: Manages the versioning of configuration data associated with different API endpoints.
- commchannel: Outlines the communication preferences and channels for the API services in different regions/countries.
- Additional: Models such as `userloginlog`, `events`, `RideDuration`, `equipment`, `publicevent`, `sound`,
  and `image` each represent an important aspect of the data managed through the Core application of the Suroga API.

Refer to Django's model field reference for a deeper understanding of field options:
https://docs.djangoproject.com/en/4.0/ref/models/fields/

Maintainer: Carlos Leandro
Last Modified:  15/3/2024

"""

#from rides.models import Ride, Booking


class time_zone(models.Model):
    """
    Model representing a time zone, which is an area of the earth that observes a standard time for legal, commercial, and social purposes.
    
    Attributes:
        Name: A human-readable name for the time zone (e.g., 'Eastern Standard Time').
        TimeZone: A string representing the actual time zone (e.g., 'EST', 'UTC-05:00').
        UTCoffset: The standard offset from UTC time in hours for this time zone.
    """
    # Define fields for the time_zone model with validation rules and help text for form rendering.
    Name = models.CharField(max_length=100,  blank=False, help_text = "Name")
    TimeZone = models.CharField(max_length=100,  blank=False,  help_text = "TimeZone")
    UTCoffset = models.DecimalField(max_digits=2, decimal_places=0,default=0, help_text = "UTC offset") 
      
    class Meta:
        # Define how multiple instances of the model should be referred to in the admin interface.
        verbose_name_plural = "Time zones"
    def __str__(self):
        # Return the model's name as its string representation, which is displayed in the admin interface and when the model is cast to a string.
        return self.Name

class Language(models.Model):
    """
    Model representing a language supported by the service.
    
    Attributes:
        Name: The name of the language (e.g., 'English', 'Portuguese').
        Code: A short code representing the language (e.g., 'en' for English, 'pt' for Portuguese).
    """
    # Each field definition, such as 'CharField' specifies the type of data and how it should be stored in the database.
    Name = models.CharField(max_length=100, unique=True, blank=False, help_text = "")
    Code = models.CharField(default='', max_length=5, blank=True, help_text = "")
    class Meta:
        verbose_name_plural = "Languages"
    def __str__(self):
        return self.Name

class Currency(models.Model):
    """
    Model representing a currency used in financial transactions.
    
    Attributes:
        Name: A full human-readable name of the currency (e.g., 'Euro').
        Currency: A string identifier for the currency unit (e.g., 'EUR' for Euro).
        CurrencySymbol: The symbol used for the currency (e.g., '€' for Euro).
        SymbolRight: A boolean indicating if the currency symbol should be displayed to the right of amounts (e.g., 'True' might indicate a format like '100€').
    """
    Name = models.CharField(max_length=100, unique=True, blank=False, help_text = "")
    Currency = models.CharField(default='EURO', max_length=30, blank=False, help_text = "Country currency.") 
    CurrencySymbol = models.CharField(default='€', max_length=5, blank=False, help_text = "Country currency Sym.") 
    SymbolRight = models.BooleanField(default=False, help_text = "True if country is open to registration.")
     
    class Meta:
        verbose_name_plural = "Currencies"
    def __str__(self):
        return self.Name

class country(models.Model):
    """
    Model representing a country where services are available.
    
    Attributes:
        Name: The name of the country.
        Currency: A ForeignKey reference to a Currency instance, representing the currency used in this country.
        Language: A ForeignKey reference to a Language instance, representing the official or prevalent language(s) of this country.
        PhoneCode: The international telephone dialing prefix for this country.
        TimeZone: A ForeignKey reference to a TimeZone instance, representing the time zone(s) utilized in this country.
        VAT: The standard rate of Value-Added Tax (VAT) applied to goods and services in this country.
        GPS_latitude: Central geographic latitude used for mapping services.
        GPS_longitude: Central geographic longitude used for mapping services.
        ZoomLevel: Default zoom level used when displaying this country on a map.
        GoogleCode: A country-specific code used by Google services.
    """
    Name = models.CharField(max_length=100, unique=True, blank=False, help_text = "Country Nome")
    Currency =  models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Country Currency") 
    Language =  models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Country Language") 
    PhoneCode = models.CharField(max_length=5, unique=True, blank=False, help_text = "Country Phone Code")
    time_zone =  models.ForeignKey(time_zone, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Country time zone") 
    VAT = models.DecimalField(max_digits=5, decimal_places=2,default=23.0, help_text = "Country VAT") 
    GPS_latitude = models.DecimalField(max_digits=12, decimal_places=8, default=0, help_text = "Country central GPS latitude") 
    GPS_longitude = models.DecimalField(max_digits=12, decimal_places=8, default=0, help_text = "Country central GPS latitude") 
    ZoomLevel = models.IntegerField(default=15, help_text = "Country Zoom Level") 
    GoogleCode = models.CharField(default='', max_length=2, blank=True, help_text = "Country Google Code")
    
    class Meta:
        verbose_name_plural = "Countries"
    def __str__(self):
        return self.Name

class districtregion(models.Model):
    """
    Represents a geographical district or region where the Suroga service operates.
    
    Attributes:
        Name: The official name of the district or region.
        GPS_latitude: The central latitude coordinate used for location purposes.
        GPS_longitude: The central longitude coordinate used for location purposes.
        ZoomLevel: A value indicating the default zoom level on maps for this region.
        GoogleCode: A two-letter code representing the region for use with Google services.
    """
    Country = models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Country", related_name='districtregion_country') 
    Name = models.CharField(default='',max_length=100, help_text = "Service Disctrict")
    GPS_latitude = models.DecimalField(max_digits=12, decimal_places=8, default=0, help_text = "District central GPS latitude") 
    GPS_longitude = models.DecimalField(max_digits=12, decimal_places=8, default=0, help_text = "District central GPS latitude") 
    ZoomLevel = models.IntegerField(default=15, help_text = "District Zoom Level") 
    GoogleCode = models.CharField(default='', max_length=2, blank=True, help_text = "District Google Code")
    
    class Meta:
        verbose_name_plural = "District/Region"
    def __str__(self):
        return self.Name

class citymunicipality(models.Model):
    """
    Represents a city or municipality within a district or region covered by the service.
    
    Attributes:
        Name: The official name of the city or municipality.
        districtregion: A ForeignKey that links to the parent district or region.
        GPS_latitude: The central latitude coordinate of the city or municipality.
        GPS_longitude: The central longitude coordinate of the city or municipality.
        ZoomLevel: A value indicating the default zoom level on maps for this locality.
        GoogleCode: A two-letter code representing the city for use with Google services.
    """
    Name = models.CharField(default='',max_length=100, help_text = "Service Municipality")
    districtregion =  models.ForeignKey(districtregion, on_delete=models.CASCADE, null=False, blank=False, help_text = "Municipality District", related_name='municipality_district') 
    GPS_latitude = models.DecimalField(max_digits=12, decimal_places=8, default=0, help_text = "Municipality central GPS latitude") 
    GPS_longitude = models.DecimalField(max_digits=12, decimal_places=8, default=0, help_text = "Municipality central GPS latitude") 
    ZoomLevel = models.IntegerField(default=15, help_text = "Municipality Zoom Level") 
    GoogleCode = models.CharField(default='', max_length=2, blank=True, help_text = "Municipality Google Code")
    
    class Meta:
        verbose_name_plural = "City/Municipality"
    def __str__(self):
        return self.Name

class usertype(models.Model):
    """
    Represents a category or type of user within the platform, used to define roles and permissions.
    
    Attributes:
        UserTypeName: A label describing the type of user, defining their role within the service.
    """
    UserTypeName = models.CharField(max_length=50, unique=True, blank=False, help_text = "User Type")
     
    class Meta:
        verbose_name_plural = "User Type"
    def __str__(self):
        return self.UserTypeName

class userprofile(models.Model):
    """
    Extends the base User model with additional attributes specific to the Suroga service.
    
    Attributes:
        user: A ForeignKey link to the associated User instance.
        PlantformUserType: ForeignKey to the usertype, indicating the role of the user on the platform.
        email_confirmed: Boolean indicating if the user's email address has been confirmed.
        Tele_confirmed: Boolean indicating if the user's telephone number has been confirmed.
        is_blocked: Boolean indicating if the user has been blocked from the service.
        Language1: ForeignKey to a Language, representing the user's primary language.
        Language2: ForeignKey to another Language for bilingual users, representing their second language.
        Paymentupdated: Boolean indicating if payment info, such as details with Stripe, is up-to-date.
    """

    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name='profile_user')    
    
    #Users registered on the service
    PlantformUserType = models.ForeignKey(usertype, on_delete=models.SET_NULL, null=True, blank=True, default="", help_text = "User type", related_name='user_type') 
    
    email_confirmed = models.BooleanField(default=False, help_text = "True if email was confirmed.")
    Tele_confirmed = models.BooleanField(default=False, help_text = "True if telephone was confirmed.")
    
    # User is blocked
    is_blocked = models.BooleanField(default=True, help_text = "True if user was is_blocked.")

    # User default language
    Language1 = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, default="", help_text = "Frist Language", related_name='user_language1') 
    Language2 = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, default="", help_text = "Second Language", related_name='user_language2') 
        
    # Stripe info updated
    Paymentupdated = models.BooleanField(default=True, help_text = "True if user info was updated on Stripe.")

    # User hash
    def __str__(self):
        return str(self.user)

class userloginlog(models.Model):
    """
    Represents a log entry for a user login attempt.
    
    Attributes:
        user: A reference to the User who attempted the login.
        IP: The IP address from which the login attempt was made.
        user_agent: Detailed string representing the browser or client software used.
        local: The locale from which the login attempt was made (if available).
        region: The region from which the login attempt was made.
        country: The country from which the login attempt was made.
        lon: The longitude of the geolocation of the IP address.
        lat: The latitude of the geolocation of the IP address.
        geo_located: A boolean indicating whether the geolocation was successful.
        RegistrationDate: The date and time when the login attempt occurred.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default="", help_text = "payment_user") 
    IP = models.CharField(max_length=15, help_text = "IP")
    user_agent = models.TextField(default='', help_text = "User agent")
    local = models.CharField(max_length=50, default='', help_text = "Local")
    region = models.CharField(max_length=50, default='',)
    country = models.CharField(max_length=100,help_text = "Country")
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    geo_located = models.BooleanField(default=False, help_text = "True if IP is geolocated.")
    RegistrationDate = models.DateTimeField(default=timezone.now, editable=True, help_text = "Access Date.")
 
    class Meta:
        verbose_name_plural = "User login log"
    def __str__(self):
        return self.user.username + " (" + self.IP + ") at " + str(self.RegistrationDate)


class events(models.Model):
    """
    Represents an API request event.
    
    Attributes:
        user: A reference to the User associated with the event.
        Type: The type of the event (e.g., CRUD operation).
        Registration: The date and time when the event occurred.
        Request_Id: A unique identifier for the request.
        Request: The actual data of the request.
    """

    # User profile
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='event_user')    
    Type = models.CharField(max_length=10,  blank=False, help_text = "Event Type")
    Registration = models.DateTimeField(default=timezone.now)
    Request_Id = models.CharField(max_length=20, blank=True, editable=True, help_text = "Request ID")
    Request = models.TextField(max_length=1000, blank=True, help_text = "The request")

      
    class Meta:
        verbose_name_plural = "API request"
    def __str__(self):
        return str(self.Registration)


class RideDuration(models.Model):
    """
    Represents a predefined list of ride durations.
    
    Attributes:
        Duration: The time duration for the ride.
        Token: An authentication token or identifier associated with the ride duration.
    """
    Duration = models.DurationField(null=False,
                                    blank=False,
                                    default='00:30:00',
                                    verbose_name=('timeslot_duration'),
                                    help_text=('HH:[MM]format')
                                    )
    Token = models.CharField(default='',max_length=30,  help_text = "Token")
    
    class Meta:
        verbose_name_plural = "Ride Duration"
    def __str__(self):
        return str(self.Duration)

class equipment(models.Model):
    """
    Represents an item of equipment available for use during rides or events.
    
    Attributes:
        Name: Name of the piece of equipment.
        Token: An authentication token or identifier associated with the equipment.
    """
    Name = models.CharField(max_length=30, unique=True, blank=False, help_text = "Public events type")
    Token = models.CharField(default='',max_length=30, help_text = "Token")
    
    class Meta:
        verbose_name_plural = "Equipments"
    def __str__(self):
        return self.Name

class publicevent(models.Model):
    """
    Represents a type of public event.
    
    Attributes:
        Name: Name of the public event type.
        Token: An authentication token or identifier associated with the public event.
    """
    Name = models.CharField(max_length=30, unique=True, blank=False, help_text = "Public events type")
    Token = models.CharField(default='',max_length=30,  help_text = "Token")
    
    class Meta:
        verbose_name_plural = "Public events"
    def __str__(self):
        return self.Name

class sound(models.Model):
    """
    Represents a category of sound requirements for rides or events.
    
    Attributes:
        Name: Name of the sound requirement category.
        Token: An authentication token or identifier associated with the sound requirement.
    """
    Name = models.CharField(max_length=30, unique=True, blank=False, help_text = "Sound type")
    Token = models.CharField(default='',max_length=30, help_text = "Token")
    
    class Meta:
        verbose_name_plural = "Sound requirements"
    def __str__(self):
        return self.Name

class image(models.Model):
    """
    Represents a category of image requirements for rides or events.
    
    Attributes:
        Name: Name of the image requirement category.
        Token: An authentication token or identifier associated with the image requirement.
    """
    Name = models.CharField(max_length=30, unique=True, blank=False, help_text = "Image type")
    Token = models.CharField(default='',max_length=30, help_text = "Token")
    
    class Meta:
        verbose_name_plural = "Image requirements"
    def __str__(self):
        return self.Name

class localwifi(models.Model):
    """
    Represents different types of Wi-Fi services or configurations provided at local venues or by the service.
    
    Attributes:
        Name: The name or type of the Wi-Fi service/configuration.
        Token: An identifier or access token associated with the Wi-Fi service.
    """
    Name = models.CharField(max_length=30, unique=True, blank=False, help_text = "Local wifi type")
    Token = models.CharField(default='',max_length=30,  help_text = "Token")
    
    class Meta:
        verbose_name_plural = "Local Wi-Fi"
    def __str__(self):
        return self.Name

class version(models.Model):
    """
    Tracks versions of the configuration data for different API endpoints to manage updates and changes.
    
    Attributes:
        endpoint: The name of the API endpoint.
        version: The current version number of the endpoint's configuration data.
        RegistrationDate: The date and time when the version was updated or registered.
    """
    
    endpoint = models.CharField(max_length=50, blank=False, help_text = "Endpoint name")
    version = models.IntegerField(default=0, help_text = "Version")
    RegistrationDate = models.DateTimeField(default=timezone.now, editable=False, help_text = "Date of version change")
 
    class Meta:
        verbose_name_plural = "Endpoint Version"
    def __str__(self):
        return self.endpoint


class commchannel(models.Model):
    """
    Defines communication channels such as email addresses for CRM and support, related to API services in different countries.
    
    Attributes:
        Country: A reference to a 'country' model instance indicating which country the communication channel is for.
        mail_opr: RFQ & Replies to / from Suppliers of Streamers.
        mail_api: Tec-support for API Suppliers (vs Supl Streamers).
        mail_ride: OPR Alerts & Comm between API (Suroga) & Clients API.
        RegistrationDate: The date and time when the communication channel was updated or registered.
    """
    Country = models.OneToOneField(country, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Country") 
    
    mail_opr = models.CharField(default="" , max_length=50, blank=False, help_text = "Email address for RFQ & Replies to / from Suppliers of Streamers")
    mail_api = models.CharField(default="" , max_length=50, blank=False, help_text = "Email address for Tec-support for API Suppliers (vs Supl Streamers)")
    mail_ride = models.CharField(default="" , max_length=50, blank=False, help_text = "Email address for OPR Alerts & Comm between API (Suroga) & Clients API")
    RegistrationDate = models.DateTimeField(default=timezone.now, editable=False, help_text = "Date of registration or change")
 
    class Meta:
        verbose_name_plural = "Communication Channels"
    def __str__(self):
        return self.Country.Name if self.Country else 'Unknown country'

def get_client_ip(request):
    """
    Utility function to extract the client's IP address from the request.
    
    The 'X-Forwarded-For' header is checked first to account for proxy servers. If not found, 
    'REMOTE_ADDR' is used to get the IP address.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip.split(':')[0]

def get_location_data__from_ip(ip):
    """
    Retrieves geolocation information for the provided IP address using an external API service.
    
    A private IP address will use a placeholder IP to fetch location data as local IP addresses do not have an associated location.
    """
    # if ip is local (so it's impossible to find lat/long coords and location) project will use random google ip as placeholder]
    if ipaddress.ip_address(ip).is_private:
        if hasattr(conf_settings, 'IP_PLACEHOLDER'):
            ip = conf_settings.IP_PLACEHOLDER
        else:
            ip = "216.58.201.110"
    else:
        pass

    #url = "http://ip-api.com/json/"+ip

    #locationInfo = requests.get(url).json()
    locationInfo =''
    return locationInfo

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    """
    Signal receiver for the user_logged_in signal to log user's login attempt details.
    
    It captures user's IP, user agent, and location data, creating a userloginlog instance with these details.
    """
    ip = get_client_ip(request)
    #locationInfo = get_location_data__from_ip(ip)
    locationInfo = ''
    if locationInfo:
        login = userloginlog.objects.create(
            user=user,
            IP=ip,
            user_agent=request.META['HTTP_USER_AGENT'],
            country=locationInfo["country"],
            region=locationInfo["region"],
            local=locationInfo["city"],
            lon=locationInfo["lon"],
            lat=locationInfo["lat"],
            geo_located = True
        )
    else:
        login = userloginlog.objects.create(
            user=user,
            IP=ip,
            user_agent=request.META['HTTP_USER_AGENT'],
            country='',
            region='',
            local='',
            lon=0.0,
            lat=0.0,
            geo_located = True
        )
