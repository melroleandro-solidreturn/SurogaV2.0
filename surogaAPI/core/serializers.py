
from rest_framework import routers, serializers, viewsets
#from core.models import time_zone, rating, RideDuration, ServiceType, PathType
#from core.models import PathType, Technology, Local, Language, Currency, Country
from core.models import events, time_zone, RideDuration
from core.models import  Language, Currency, country
from core.models import  districtregion, citymunicipality  
from core.models import equipment, publicevent, sound, image, localwifi 
from drf_api_logger.models import APILogsModel

"""
Core Application Serializers - Suroga API

This file contains serializers that convert complex data types, such as querysets and model instances, to native Python 
data types. The serialized data can then be easily rendered into JSON (or other content types) for API responses, or 
used for parsing incoming data in API requests. 

The serializers defined here correspond closely with the models defined in the core app's `models.py`. They ensure that 
the data representation for API communication conforms to a consistent structure and format. They also handle validation 
for incoming data used to create or update model instances.

Serializers included:
- soundSerializer: Handles sound requirements data.
- imageSerializer: Manages image requirements.
- localwifiSerializer: Processes local Wi-Fi configurations.
- eventsSerializer: Logs API interaction events.

These serializers extend Django REST Framework's ModelSerializer class and automatically generate a set of fields and 
validators based on the corresponding models. The Serializers are primarily configured to be read-only as many of the 
endpoints serve static or reference data not intended for frequent modification through the API.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014

Refer to Django REST Framework's serializer documentation for more information:
https://www.django-rest-framework.org/api-guide/serializers/
"""

# time_zoneSerializer converts time_zone instances to and from JSON.
class time_zoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = time_zone
        fields = ['pk','Name', 'TimeZone', 'UTCoffset']
        read_only_fields = fields # Prevents modification of the serialized fields.


# LanguageSerializer is responsible for the serialization process of the Language model,
# allowing for representation as JSON, used for API responses or submissions.
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['pk','Name','Code']
        read_only_fields = fields

# RideDurationSerializer serializes instances of the RideDuration model, enabling them to 
# be outputted as JSON, often necessary for interaction with frontend applications.
class RideDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideDuration
        fields = ['pk','Duration']
        read_only_fields = fields

# citymunicipalitySerializer is responsible for handling the serialization of city/municipality data.
# It includes extra fields such as GPS coordinates and a related district/region.
class citymunicipalitySerializer(serializers.ModelSerializer):  
    
    class Meta:
            model = citymunicipality
            fields = ['pk','Name','districtregion','GPS_latitude','GPS_longitude','ZoomLevel','GoogleCode']
            read_only_fields = fields

# districtregionSerializer embeds the citymunicipalitySerializer to include related city/municipality
# data nested within the representation of each district/region.
class districtregionSerializer(serializers.ModelSerializer):
    
    municipality_district = citymunicipalitySerializer(many=True, read_only=True)
    
    
    class Meta:
            model = districtregion
            fields = ['pk','Name','GPS_latitude','GPS_longitude','ZoomLevel','GoogleCode','municipality_district']
            read_only_fields = fields

# CurrencySerializer handles serialization of currency instances which may include name, code, symbol, 
# and a boolean indicating the conventional position of the currency symbol.
class CurrencySerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Currency
        fields = ['pk','Name','Currency','CurrencySymbol','SymbolRight']
        read_only_fields = fields

# CountrySerializer serializes country instances, including nested details provided by currency,
# language, and time zone serializers.
class CountrySerializer(serializers.ModelSerializer):
    
    Currency = CurrencySerializer(read_only=True)
    Language = LanguageSerializer(read_only=True)
    time_zone = time_zoneSerializer(read_only=True)

    class Meta:
        model = country
        fields = ['pk','Name','Currency','Language','PhoneCode','time_zone','VAT','GPS_latitude','GPS_longitude','ZoomLevel','GoogleCode']

# equipmentSerializer provides serialization for equipment items, including the name and a unique identifier.
class equipmentSerializer(serializers.ModelSerializer):  
    class Meta:
            model = equipment
            fields = ['pk','Name']
            read_only_fields = fields

# publiceventSerializer manages serialization of public event types, essential for endpoints which manage event-based data.
class publiceventSerializer(serializers.ModelSerializer):  
    class Meta:
            model = publicevent
            fields = ['pk','Name']
            read_only_fields = fields

# soundSerializer converts instances of the sound model to and from JSON format.
class soundSerializer(serializers.ModelSerializer):  
    class Meta:
            # Specifies the model associated with this serializer.
            model = sound
            # Defines the list of fields that should be included in the serialized output.
            fields = ['pk','Name']
            # Declares all fields as read-only, preventing modification through API requests.
            read_only_fields = fields

# imageSerializer handles serialization for image requirement objects,
# allowing them to be easily converted to JSON for API responses.
class imageSerializer(serializers.ModelSerializer):  
    class Meta:
            # Associates the serializer with the image model.
            model = image
            # Selects which fields from the image model should be included in the serialized data.
            fields = ['pk','Name']
            # Marks these fields as not writable, ensuring they can only be read through the API.
            read_only_fields = fields

# localwifiSerializer is responsible for the serialization of local Wi-Fi configuration data.
class localwifiSerializer(serializers.ModelSerializer):  
    class Meta:
            # Points to localwifi as the source model for the serializer.
            model = localwifi
            # Lists the fields to be included in the serialization process.
            fields = ['pk','Name']
            # Sets the field permissions to read-only to prevent changes via the API.
            read_only_fields = fields

# eventsSerializer is designed for creating representations of API log entries.
class eventsSerializer(serializers.ModelSerializer):  
    class Meta:
            # Sets APILogsModel as the model that backs this serializer.
            model = APILogsModel
            # Specifies the fields from APILogsModel that should appear in the serialized form.
            fields = ['pk','user','added_on','method','api','client_ip_address','status_code','execution_time','response']
            # Sets all these fields as immutable in the context of an API operation.
            read_only_fields = fields

