"""
Rides App Serializers - Suroga API

This module contains serializers for converting complex data types such as Django model instances
to native Python datatypes and then rendering those into JSON for API endpoints within the 'rides'
application of the Suroga API project. These serializers also provide deserialization, allowing
parsed data to be converted back into complex types after first validating the incoming data.

The serializers define the API representation for various models like Booking, Stock in the
contract ride market, and messaging on the Message Board.

Usage:
    These serializers are typically used in views and viewsets provided by Django REST Framework to handle
    the inbound and outbound data processing for API requests and responses.

References:
    - Django REST Framework serializers: https://www.django-rest-framework.org/api-guide/serializers/
    - ModelSerializer class: https://www.django-rest-framework.org/api-guide/serializers/#modelserializer

The file should be maintained thoughtfully, as changes to the serializers affect data validation,
serialization, and the overall input/output contracts of the API.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.views import APIView

from rides.models import bookinglog, MessageBoard, ContrSectionRideMkt, rating, ServiceCategory, ridetype, Ride, Booking

from supplier.models import servicetype, contractsection

from django.db.models import Q

from django.core import serializers as core_serializers

from core.serializers import equipmentSerializer, publiceventSerializer, localwifiSerializer, soundSerializer, imageSerializer, RideDurationSerializer

# Serializers define the API representation.

# Serializer for the Rating model
class ratingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model that defines the representation in the API.
    
    The fields attribute specifies which model fields should be included in the serialized output/input.
    """
    class Meta:
        model = rating # The model associated with this serializer
        fields = ['pk','Name','value'] # Fields that should be included in the serialized data

# Serializer for the ServiceCategory model
class servicecategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ServiceCategory model for REST API representation.
    """
    class Meta:
        model = ServiceCategory # The model associated with this serializer
        fields = ['pk','Name'] # The fields to be included

# Serializer for the RideType model
class ridetypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the RideType model to convert it to and from JSON format for API interactions.
    """
    class Meta:
        model = ridetype # The model associated with this serializer
        fields = ['pk','Name'] # The required fields

# Serializer for the Ride model
class rideCreateSerializer(serializers.ModelSerializer):

    """
    Serializer for the Ride model which defines the detailed API endpoint representation.
    
    Includes complex logic for the creation, where some fields are populated based on the current user 
    and default values. `read_only_fields` specifies fields that cannot be edited via the API.
    """
    # Primary key related field that automatically populates with the current user's id
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Ride # The model associated with this serializer
        # All the fields that can be included in the serialized form of a Ride, including read-only fields.
        fields = ['pk','user','ExternalMetaData','PayedAtRegistration','ServiceCategory','Country', 'RideDate',
        'DistrictRegion','CityMunicipality','StreetName','StreetNumber','Floor', 'ZipCode',
        'Equipment','PublicEvent','LocalWifi','Sound','Image','ExpectDuration',
        'GPS_latitude','GPS_longitude','Zoom_map','GooglePlaceID','RideType','ServiceTitle',
        'Description','RegistrationDate','GeneratePaymentLink','PaymentLink','PaymentCODE','Blocked','Canceled',
        'Deleted','NotAvailable','HashKey','Request_Id','Closed','Requisits']
        # Fields that are read-only and won't accept data during updates/creates.
        read_only_fields = ['pk','user','PayedAtRegistration','RegistrationDate','GeneratePaymentLink','PaymentLink','PaymentCODE','NotAvailable',
        'Blocked','HashKey','Request_Id']
    
    def save(self, **kwargs):
        """
        Overridden save method to include a default value for the read_only `user` field.
        """
        kwargs["user"] = self.fields["user"].get_default()   # Assign the current user as a default
        
        return super().save(**kwargs)  # Call the super class's save method to handle further operations


# Serializer for the Ride model
class rideSerializer(serializers.ModelSerializer):

    """
    Serializer for the Ride model which defines the detailed API endpoint representation.
    
    Includes complex logic for the creation, where some fields are populated based on the current user 
    and default values. `read_only_fields` specifies fields that cannot be edited via the API.
    """
    # Primary key related field that automatically populates with the current user's id
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    # equipmentSerializer, publiceventSerializer, localwifiSerializer, soundSerializer, imageSerializer, RideDurationSerializer
    ServiceCategory = servicecategorySerializer()
    RideType = ridetypeSerializer()
    Equipment = equipmentSerializer()
    PublicEvent = publiceventSerializer()
    LocalWifi = localwifiSerializer()
    Sound = soundSerializer()
    Image = imageSerializer()
    ExpectDuration = RideDurationSerializer()

    booking_count = serializers.SerializerMethodField()
    click_count = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Ride # The model associated with this serializer
        # All the fields that can be included in the serialized form of a Ride, including read-only fields.
        fields = ['pk','user','ExternalMetaData','PayedAtRegistration','ServiceCategory','Country', 'RideDate',
        'DistrictRegion','CityMunicipality','StreetName','StreetNumber','Floor', 'ZipCode',
        'Equipment','PublicEvent','LocalWifi','Sound','Image','ExpectDuration',
        'GPS_latitude','GPS_longitude','Zoom_map','GooglePlaceID','RideType','ServiceTitle',
        'Description','RegistrationDate','GeneratePaymentLink','PaymentLink','PaymentCODE','Blocked','Canceled',
        'Deleted','NotAvailable','HashKey','Request_Id','Closed','Requisits','booking_count','click_count','rate']
        # Fields that are read-only and won't accept data during updates/creates.
        read_only_fields = ['pk','user','PayedAtRegistration','RegistrationDate','GeneratePaymentLink','PaymentLink','PaymentCODE','NotAvailable',
        'Blocked','HashKey','Request_Id','booking_count','click_count','rate']

    def get_booking_count(self, obj):
        # Contar o número de logs associados com a ação 'booking'
        return obj.actionLog_ride.filter(OperationType='booked').count()  
   
    def get_click_count(self, obj):
        # Contar o número de logs associados com a ação 'click'
        return obj.actionLog_ride.filter(OperationType='Click').count()  
       
    def get_rate(self, obj):
        # Compute the mean rate
        return obj.Booking_booking.filter(Completed=True).count()  
   

# Serializer for the Ride model
class bookingCreateSerializer(serializers.ModelSerializer):

    """
    Serializer for the Ride model which defines the detailed API endpoint representation.
    
    Includes complex logic for the creation, where some fields are populated based on the current user 
    and default values. `read_only_fields` specifies fields that cannot be edited via the API.
    """
    # Primary key related field that automatically populates with the current user's id
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Booking # The model associated with this serializer
        # All the fields that can be included in the serialized form of a Ride, including read-only fields.
        fields = ['pk','user','ExternalMetaData','ServiceCategory','Country', 'RideDate',
        'DistrictRegion','CityMunicipality','StreetName','StreetNumber','Floor', 'ZipCode',
        'Equipment','PublicEvent','LocalWifi','Sound','Image','ExpectDuration',
        'GPS_latitude','GPS_longitude','Zoom_map','GooglePlaceID','RideType','ServiceTitle',
        'Description','RegistrationDate','GeneratePaymentLink','PaymentLink','PaymentCODE','Blocked','Canceled',
        'Deleted','HashKey','Request_Id']
        # Fields that are read-only and won't accept data during updates/creates.
        read_only_fields = ['pk','user','RegistrationDate','GeneratePaymentLink','PaymentLink','PaymentCODE',
        'Blocked','HashKey','Request_Id']
    
    def save(self, **kwargs):
        """
        Overridden save method to include a default value for the read_only `user` field.
        """
        kwargs["user"] = self.fields["user"].get_default()   # Assign the current user as a default
        
        return super().save(**kwargs)  # Call the super class's save method to handle further operations



# Serializer for Booking Model
class bookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model to handle serialization for API input/output.
    
    Specifies fields to include in the serialized form, with certain fields set as read-only.
    Includes default fields such as the current user, which are automatically populated.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    ServiceCategory = servicecategorySerializer()
    RideType = ridetypeSerializer()
    Equipment = equipmentSerializer()
    PublicEvent = publiceventSerializer()
    LocalWifi = localwifiSerializer()
    Sound = soundSerializer()
    Image = imageSerializer()
    ExpectDuration = RideDurationSerializer()

    class Meta:
        model = Booking # Define the associated model
        # Define fields that this serializer should process
        fields = [
            'pk',
            'user',
            'ExternalMetaData',

            'ride',
            'ServiceTitle',
            'Description',

            'Country',
            'DistrictRegion',
            'CityMunicipality',
            'StreetName',
            'StreetNumber',
            'Floor',

            'ZipCode',
            'GPS_latitude',
            'GPS_longitude',
            'Zoom_map',
            'GooglePlaceID',

            'ServiceCategory',
            'RideType',

            'RideDate', 
            'Image',
            'Sound',
            'Equipment',
            'LocalWifi',
            'PublicEvent',
            'ExpectDuration',
            
            'APIrequiresMettingURL',
            'MeetingURL',
            'MeetingPasswd',
            'RegistrationDate',
            'Blocked',
            'Canceled',
            'Deleted',
            'ServiceTitle',
            
            'Description',
            'FinalDuration',
            'ExtraPrice',
            'SelectStock',
            'Completed',
            'StockSelected',
            'CanceledAgent',
            'RequisitsSatisfied',
            'Expired',
            'Error',
            'Disputed',
            'InvitationSend',
            'InvitationAccepted',
            'closed',
            
            'SystemInfo',
            'ErrorMessages',
            
            'GeneratePaymentLink',
            'PaymentLink',
            'PaymentCODE',

            'APIrequiresDashboardURL',
            'DashboardClientURL',
            'ClientKey',
            'DashboardSurrogateURL',
            'SurrogateKey',
            
            'ClientRank',

            'RideStarted',
            'RideEnded',
            'RideStartDate',
            'RideEndDate',
            'HashKey',
            'Request_Id',
            'Stock_Id'
            ]
        # Fields that will be read-only once a Booking instance is created
        read_only_fields = [
            'pk',
            'user',
            'ExpectDuration',
            'RegistrationDate',
            'Blocked',
            'Completed',
            'Expired',
            'Error',
            'Disputed',
            'InvitationSend',
            'InvitationAccepted',
            'SystemInfo',
            'ErrorMessages',
            'GeneratePaymentLink',
            'PaymentLink',
            'PaymentCODE',
            'APIrequiresDashboardURL',
            'DashboardClientURL',
            'ClientKey',
            'DashboardSurrogateURL',
            'SurrogateKey',
            'HashKey'
            ]

    #
    #def validate_rute(self, value):
    #    """
    #    Check if ride is valide
    #    """
    #    obj = Ride.objects.get(pk=value.pk)
    #    if obj.user != self.fields["user"].get_default():
    #        raise serializers.ValidationError("The ride is invalide")
    #    return value
    #
    def save(self, **kwargs):
        """
        Custom save method to include default value for the read-only `user` field before
        saving a new Booking instance to the database.
        """
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)

# Serializer for the ContrSectionRideMkt Model    
class stockSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contract Section Ride Market model.

    It represents the structure of a stock item for Ride within the API, 
    specifying the fields included and which ones are read-only.
    """
    class Meta:
        model = ContrSectionRideMkt
        fields = ['pk','Name','rank','miss','Ride','TotalPrice','HashKey','Selected','RequiredConfigTime','setting']
        read_only_fields = ['pk','Name','rank','miss','Ride','TotalPrice','HashKey','RequiredConfigTime','setting']

# Serializer for the MessageBoard Model
class MessageBoardSerializer(serializers.ModelSerializer):
    """
    Serializer for the MessageBoard model detailing the API representation,
    which fields are included, and the default current user applied to the `user` field.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = MessageBoard
         #List of fields included in the serialization process
        fields = ['pk','user','booking','SendByClient','Text','Read','deleted','Abuse','Date']
        # Fields that are not editable and act as read-only
        read_only_fields = ['pk','user','booking','SendByClient','Text','Read','deleted','Abuse','Date']