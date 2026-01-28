"""
Rides App ViewSets - Suroga API

This module contains the viewsets for the 'rides' application within the Suroga API.
ViewSets in Django REST Framework provide a way to combine logic for a set of related views.
These classes define the behavior and permissions for API endpoints associated with Ride management,
including booking of rides, management of ride stock items, and handling of messages on the message board.

Usage:
    These viewsets are used to create RESTful APIs and are typically routed in the app's urls.py file.
    They provide a rich interface for interacting with the models over HTTP with JSON.

Features:
    - Standard CRUD operations for both stock items and messages via ModelViewSet.
    - Custom actions for additional business logic like selecting, reading, and deleting items.
    - Token-based authentication and permission classes for protected API access.

References:
    - Django REST Framework ViewSets: https://www.django-rest-framework.org/api-guide/viewsets/
    - Django Authentication: https://docs.djangoproject.com/en/4.0/topics/auth/default/
    - Permissions: https://www.django-rest-framework.org/api-guide/permissions/

The classes and methods should be carefully maintained and extended with caution to ensure the API's integrity and consistency across different clients.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""

import json
import datetime
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.utils import timezone

from django.core import serializers as core_serializers 

from rides.models import bookinglog, MessageBoard, ContrSectionRideMkt, Booking,rating, ServiceCategory, Ride, ridetype
from rides.serializers import MessageBoardSerializer, stockSerializer, ratingSerializer, servicecategorySerializer, ridetypeSerializer,rideCreateSerializer, rideSerializer
from rides.serializers import bookingCreateSerializer, bookingSerializer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from core.extras import EmailThread 
from rides.extras import book_room_async
from django.conf import settings

from supplier.models import  servicetype, contractsection
from rides.models import MessageBoard, Ride, ContrSectionRideMkt
from core.models import publicevent, localwifi, equipment, image, sound, RideDuration, country, districtregion, citymunicipality,  commchannel
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.db import connection

from django.db import transaction

import logging

from django.core.mail import send_mail

from django.core.exceptions import ObjectDoesNotExist as DoesNotExist

# rating: ViewSets define the view behavior.
class ratingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that provides access to rating operations.

    It allows for the retrieval, creation, update, and deletion of rating entries.
    Authentication is enforced via token, and only authenticated users can interact with this viewset.
    

    Retrieve: ['pk','Name','value']
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = rating.objects.all()
    serializer_class = ratingSerializer

# Service Category: ViewSets define the view behavior.
class servicecategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows operations on service categories.

    Provides a standard interface for CRUD operations on the ServiceCategory model items.
    

    Retrieve: ['pk','Name']
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ServiceCategory.objects.all()
    serializer_class = servicecategorySerializer

# ridetype: ViewSets define the view behavior.
class ridetypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling ride types.

    Accessible to authenticated users to view, create, modify, or delete ride types.
    

    Retrieve: ['pk','Name']
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ridetype.objects.all()
    serializer_class = ridetypeSerializer

def loadset(rideSet):
    """
    Aggregates different ride set items into a unique set.
    
    It adds equipment, extras, and channel information into a set, excluding any empty strings.
    
    Args:
        rideSet (dict): A dictionary containing 'equipment', 'extras', and 'channel' keys.

    Returns:
        set: A set containing unique service items.
    """
    # Initialize a set and gather service items from rideSet
    serviceSet = set()
    serviceSet.add(rideSet['equipment'])
    serviceSet = serviceSet | (set(rideSet['extras']) - {''})
    serviceSet.add(rideSet['channel'])
    return serviceSet

def price(sectioVariant, date, duration, price_type):
    """
    Calculates the price based on section variant configurations.

    Args:
        sectioVariant (str): A JSON string representing variant configurations including pricing details.
        date (datetime): The starting date and time of the service.
        duration (int): The duration of the service in minutes.
        price_type (str): A string representing the type of price to apply.

    Returns:
        float: The calculated price based on the provided parameters.
    """
    data = json.loads(sectioVariant)[0]
    if 'time_in' in data:
        inTime, price1, price2 = data['time_in']
        if 'time_out' in data:
            outTime1, outTime2 = data['time_out']

        startTime = date.time()

        endTime = (date + datetime.timedelta(minutes = duration)).time()

        if datetime.time.fromisoformat(inTime[0]) <= startTime <= datetime.time.fromisoformat(inTime[1]) and datetime.time.fromisoformat(inTime[0]) <= endTime <= datetime.time.fromisoformat(inTime[1]):
            return price1
        return price2
    if 'price' in data:
        return data['price']
    return 0



# Ride: ViewSets define the view behavior.
class rideViewSet(viewsets.ModelViewSet): 
    """
    A viewset that provides the standard actions to be performed on the Ride model instances.

    Custom actions for canceling, deleting, requesting a payment link, 
    and closing a ride are defined to accommodate specific business logic.
    
    
    The create method is overridden to include custom logic for ride creation. This logic involves sending notifications, validation of data before saving the ride, and determining the available stock based on requisites. If threading is used to send emails, ensure that the threading implementation is imported and handled correctly to prevent blocking the request/response cycle. Error handling is also done within the method, which dictates the responses returned to the client.

    Custom actions like cancel, delete, paymentlink, and close are added to the rideViewSet using the @action decorator. These actions extend the functionality of the viewset beyond the standard CRUD operations, providing endpoints for ride-specific business actions and reflect state changes that may happen to a ride after it's initially created.

    The get_queryset method has been customized to filter queryset dynamically based on query parameters passed in the request. This enables frontend clients to filter rides based on specific criteria supplied by the user.

    It's important to note that sending emails and performing business logic in the viewset methods should be optimized so they don't affect the performance of the application. Long-running tasks should ideally be handled asynchronously, outside the request/response cycle (e.g., by using Django's background task processing capabilities or a task queue like Celery).

    Additionally, this code assumes that a function named loadset, a model named ContrSectionRideMkt and serializers named rideSerializer and stockSerializer are defined somewhere in the project. The queryset filtering in get_queryset also refers to models country, districtregion, and citymunicipality which must be imported to function correctly. Also, make sure to import the necessary methods, such as DoesNotExist exception, to handle specific model query exceptions.
    """
    # Token authentication and the requirement that users are authenticated to access this viewset
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return rideCreateSerializer
        return rideSerializer
    
    def createTEST(self, request, *args, **kwargs):
        """
        Overridden create method with additional logic to send emails and process booking conditions, etc.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({"Fail": "blablal"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        
        pk = int(serializer.data['pk'])
        ServiceTitle = serializer.data['ServiceTitle']
        
        #if CountryID:
        #    comm = commchannel.objects.filter(Country = CountryID)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET

        message = render_to_string('emails_backoffice/ride_registration.html', {
            'UserID': request.user.pk,
            'User': request.user.username,
            'RideID': pk,  
            'Title': ServiceTitle, 
            'URL': settings.DOMAIN+'/admin/rides/ride/'+str(pk)+'/change/', 
            'STATUS': 'Registred',
        })
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride registration',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        ###
        # Create stock list
        ###
        StreetName = serializer.validated_data['StreetName']

        if not StreetName:
            return Response({"Success": 0, "Error": 'L000', "Message": "Street name required by Suroo API","ride": serializer.data,"stock":[]})


        # Services requirements
        #ExpectDuration = serializer.validated_data['ExpectDuration']

        # Services requirements
        Country = serializer.validated_data['Country']
        ServiceCategory = serializer.validated_data['ServiceCategory']
        RideType = serializer.validated_data['RideType']
        #PublicEvent = serializer.validated_data['PublicEvent']
        #LocalWifi = serializer.validated_data['LocalWifi']
        #Sound = serializer.validated_data['Sound']
        #Image = serializer.validated_data['Image']
        #ExpectDuration = serializer.validated_data['ExpectDuration']
        
        RideDate = serializer.validated_data['RideDate']
        
        Requisits = serializer.validated_data['Requisits']

        
        RequestSet = loadset(json.loads(Requisits)[0]) 

        #services = servicetype.objects.filter(Q(Duration=ExpectDuration),Q(Image=Image),Q(Sound=Sound),Q(LocalWifi=LocalWifi),Q(PublicEvent=PublicEvent))
        services = servicetype.objects.all()
        

        servicesRank = []
        for service in services:
            setting = json.loads(service.ServiceSetting)
            serviceSet = loadset(setting[0])
            rank = RequestSet - serviceSet
            servicesRank.append((len(rank),service,rank,serviceSet))

        # Local
        
        CountryName = serializer.validated_data['Country']       
        if not CountryName:
            return Response({"Success": 0, "Error": 'L001', "Message": "Country required by Suroo API","ride": serializer.data,"stock":[]})

        DistrictRegionName = serializer.validated_data['DistrictRegion']
        if not DistrictRegionName:
            return Response({"Success": 0, "Error": 'L002', "Message": "District or region name required by Suroo API","ride": serializer.data,"stock":[]})

        CityMunicipalityName = serializer.validated_data['CityMunicipality']
        if not CityMunicipalityName:
            return Response({"Success": 0, "Error": 'L003', "Message": "City and municipality name required by Suroo API","ride": serializer.data,"stock":[]})

        try:
            CountryID = country.objects.get(Name = CountryName)
        except DoesNotExist:
            return Response({"Success": 0, "Error": 'L011', "Message": "Country isn't covered by Suroo API", "ride": serializer.data,"stock":[]})

        try:
            DistrictRegionID = districtregion.objects.get(Name = DistrictRegionName)
        except DoesNotExist:
            return Response({"Success": 0, "Error": 'L012', "Message": "District or region isn't covered by Suroo API", "ride": serializer.data,"stock":[]})

        try:
            CityMunicipalityID = citymunicipality.objects.get(Name = CityMunicipalityName)
        except DoesNotExist:
            return Response({"Success": 0, "Error": 'L013', "Message": "City or municipality isn't covered by Suroo API", "ride": serializer.data,"stock":[]})

        contracts = contractsection.objects.filter(Q(is_active=True), Q(Country=CountryID), Q(DistrictRegion=DistrictRegionID) | Q(DistrictRegion__isnull = True), Q(CityMunicipality=CityMunicipalityID) | Q(CityMunicipality__isnull = True)) 


        stock={}
        for rank, record, miss, serviceSet in servicesRank:
            stock[record.pk]={'Name':record.Name, 'rank': rank, 'miss':miss, 'serviceSet': serviceSet, 'Contracts':{}}
            for item in contracts: 
                if item.contract.contract_type.pk==1:
                    if 1 not in stock[record.pk]:
                        stock[record.pk]['Contracts'][1]=[]
                    stock[record.pk]['Contracts'][1].append(item)

                if record.ContractB and item.contract.contract_type.pk==2:
                    if 2 not in stock[record.pk]:
                        stock[record.pk]['Contracts'][2]=[]
                    stock[record.pk]['Contracts'][2].append(item)

                if record.ContractC and item.contract.contract_type.pk==3:
                    if 3 not in stock[record.pk]:
                        stock[record.pk]['Contracts'][3]=[]
                    stock[record.pk]['Contracts'][3].append(item)

                if record.ContractD and item.contract.contract_type.pk==4:
                    if 4 not in stock[record.pk]:
                        stock[record.pk]['Contracts'][4]=[]
                    stock[record.pk]['Contracts'][4].append(item)

                if record.ContractE and item.contract.contract_type.pk==5:
                    if 5 not in stock[record.pk]:
                        stock[record.pk]['Contracts'][5]=[]
                    stock[record.pk]['Contracts'][5].append(item)

                if record.ContractF and item.contract.contract_type.pk==6:
                    if 6 not in stock[record.pk]:
                        stock[record.pk]['Contracts'][6]=[]
                    stock[record.pk]['Contracts'][6].append(item)
 
        
        rideIdx = Ride.objects.get(pk=pk)
        stockMkt = []
        for idS in stock:
            item = stock[idS]['Contracts']
            Mkt = ContrSectionRideMkt()
            Mkt.miss = json.dumps(list(stock[idS]['miss']))
            Mkt.rank = stock[idS]['rank']
            Mkt.setting = json.dumps(list(stock[idS]['serviceSet']))
            Mkt.Name = stock[idS]['Name']
            Mkt.user = request.user
            Mkt.Ride = rideIdx
            Mkt.TotalPrice = 0
            Mkt.RequiredConfigTime = 0
            for id in item:
                PriceItem = 0
                if id == 1:
                    Mkt.ContractSectionA = item[id][0]
                    PriceItem = price(item[id][0].variante,RideDate,30,1) 
                    Mkt.ContractPriceA = PriceItem

                if id == 2:
                    Mkt.ContractSectionB = item[id][0]
                    PriceItem = price(item[id][0].variante,RideDate,30,1)
                    Mkt.ContractPriceB = PriceItem

                if id == 3:
                    Mkt.ContractSectionC = item[id][0]
                    PriceItem = price(item[id][0].variante,RideDate,30,1)
                    Mkt.ContractPriceC = PriceItem

                if id == 4:
                    Mkt.ContractSectionD = item[id][0]
                    PriceItem = price(item[id][0].variante,RideDate,30,1)
                    Mkt.ContractPriceD = PriceItem

                if id == 5:
                    Mkt.ContractSectionE = item[id][0]
                    PriceItem = price(item[id][0].variante,RideDate,30,1)
                    Mkt.ContractPriceE = PriceItem

                if id == 6:
                    Mkt.ContractSectionF = item[id][0]
                    PriceItem = price(item[id][0].variante,RideDate,30,1)
                    Mkt.ContractPriceF = PriceItem

                Mkt.TotalPrice += PriceItem
                Mkt.RequiredConfigTime = max(Mkt.RequiredConfigTime,item[id][0].RequiredMaxConfigTime)
            
            Mkt.save()
            stockMkt.append(Mkt)
        
        stockMkt = ContrSectionRideMkt.objects.filter(Ride = rideIdx)
        
        if len(stockMkt) == 0:
            return Response({"Success": 0, "Error": 'S020', "Message": "Service isn't available by Suroo API for your location.", "ride": serializer.data,"stock":[]})

        # match services
        #kwargs["stock"] = contracts

        return Response({"Success": 1, "stock":stockSerializer(stockMkt,many=True).data, "ride": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    # A custom action for canceling a ride
    @action(detail=True, methods=['get'], name='Cancel ride')
    def cancel(self, request, pk=None):
        try:
            with transaction.atomic():
                # Ride cancellation logic including email notification goes here...
                ride = self.get_object()
                ride.Canceled = True
                ride.save()
                #if self.Country:
                #    comm = commchannel.objects.filter(Country = self.ride.Country)
                #    mail_backoffice = comm.mail_ride
                #else:
                mail_backoffice = settings.EMAILMARKET

                message = render_to_string('emails_backoffice/ride_status_changed.html', {
                    'UserID': ride.user.pk,
                    'User': ride.user.username,
                    'RideID': ride.pk,  
                    'Title': ride.ServiceTitle,
                    'URL': settings.DOMAIN+'/admin/rides/ride/'+str(ride.pk)+'/change/', 
                    'STATUS': 'Cancel',
                })
                # Define email message
                email_message = {
                    "message": {
                        "subject": 'Support: Ride cancel',
                        "body": {
                            "contentType": "Text",
                            "content": message
                        },
                        "toRecipients": [
                            {
                                "emailAddress": {
                                    "address":  mail_backoffice
                                }
                            }
                        ]
                    }
                }
                
                EmailThread(email_message).start()
        
            return Response({'status': 'OK','ride': core_serializers.serialize('json', [ride,])})
        
        except Exception as e:
            logging.error(f"Ride cancellation failed: {e}")
            return Response({'status': 'error', 'detail': str(e)}, status=500)
      
    # A custom action for deleting a ride
    @action(detail=True, methods=['get'], name='Remove ride')
    def delete(self, request, pk=None):
        # Ride deletion logic goes here...
        ride = self.get_object()
        booking = Booking.objects.filter(ride=ride)
        if booking:
            return Response({'status': 'ERROR','Error':'100','Message': 'You have a assigment to this ride','ride':  core_serializers.serialize('json', [ride,])})
        ride.Deleted = True # add condition
        ride.save()

        log = bookinglog()
        log.user = request.user
        log.OperationType = "delete"
        log.Ride = ride
        log.Booking = None
        log.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET

        message = render_to_string('emails_backoffice/ride_status_changed.html', {
            'UserID': ride.user.pk,
            'User': ride.user.username,
            'RideID': ride.pk,  
            'Title': ride.ServiceTitle,
            'URL': settings.DOMAIN+'/admin/rides/ride/'+str(ride.pk)+'/change/', 
            'STATUS': 'Delete',
        })
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride deleted',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()
        return Response({'status': 'OK','ride': core_serializers.serialize('json', [ride,])})

    # A custom action for log a booked
    @action(detail=True, methods=['get'], name='Request payment link')
    def booked(self, request, pk=None):

        ride = self.get_object()
        
        log = bookinglog()
        log.user = request.user
        log.OperationType = "booked"
        log.Ride = ride
        log.Booking = None
        log.save()

        return Response({'status': 'OK','action': 'booked'})

    # A custom action for log a click
    @action(detail=True, methods=['get'], name='Record click')
    def click(self, request, pk=None):

        ride = self.get_object()
        
        log = bookinglog()
        log.user = request.user
        log.OperationType = "Click"
        log.Ride = ride
        log.Booking = None
        log.save()

        return Response({'status': 'OK','action': 'click'})

    # A custom action for log a cotation
    @action(detail=True, methods=['get'], name='Request cotation')
    def cotation(self, request, pk=None):

        ride = self.get_object()
        
        log = bookinglog()
        log.user = request.user
        log.OperationType = "cotation"
        log.Ride = ride
        log.Booking = None
        log.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET

        message = render_to_string('emails_backoffice/ride_paymentlink.html', {
            'UserID': ride.user.pk,
            'User': ride.user.username,
            'RideID': ride.pk,  
            'Title': ride.ServiceTitle, 
            'PaymentLink': ride.PaymentLink,
            'URL': settings.DOMAIN+'/admin/rides/ride/'+str(ride.pk)+'/change/', 
            'STATUS': 'Booked',
        })

        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride cotation',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK','action': 'cotation'})

    # A custom action for requesting a payment link
    @action(detail=True, methods=['get'], name='Request payment link')
    def paymentlink(self, request, pk=None):
        # Payment link request logic goes here...
        ride = self.get_object()
        ride.GeneratePaymentLink = True # reques payment link
        ride.PaymentLink = 'xxx999xxx'
        ride.save()

        log = bookinglog()
        log.user = request.user
        log.OperationType = "PaymentLink"
        log.Ride = ride
        log.Booking = None
        log.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET

        message = render_to_string('emails_backoffice/ride_paymentlink.html', {
            'UserID': ride.user.pk,
            'User': ride.user.username,
            'RideID': ride.pk,  
            'Title': ride.ServiceTitle, 
            'PaymentLink': ride.PaymentLink,
            'URL': settings.DOMAIN+'/admin/rides/ride/'+str(ride.pk)+'/change/', 
            'STATUS': 'Paymentlink',
        })
        
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride Payment Link',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK','ride': core_serializers.serialize('json', [ride,])})

    # A custom action for closing a ride
    @action(detail=True, methods=['get'], name='Close ride')
    def close(self, request, pk=None):
        # Ride closing logic goes here...
        ride = self.get_object()
        ride.Closed = True
        ride.save()

        log = bookinglog()
        log.user = request.user
        log.OperationType = "Closed"
        log.Ride = ride
        log.Booking = None
        log.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/ride_status_changed.html', {
            'UserID': ride.user.pk,
            'User': ride.user.username,
            'RideID': ride.pk,  
            'Title': ride.ServiceTitle, 
            'URL': settings.DOMAIN+'/admin/rides/ride/'+str(ride.pk)+'/change/',
            'STATUS': 'Close',
        })
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support:  Ride Closed',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK', 'ride': core_serializers.serialize('json', [ride,])})
   
    def get_queryset(self):
        """
        Custom queryset filtering based on the request's parameters.

        Filters applied include Country, DistrictRegion, CityMunicipality, ServiceCategory, 
        RideType, and flags such as Blocked, Canceled, and Deleted, among others.
        """
        account_id = self.request.query_params.get('account_id')
        key = self.request.query_params.get('key')

        if not account_id and not key:
            queryset = Ride.objects.filter(user=self.request.user)

        elif 'sqlite' in connection.settings_dict['ENGINE']:
            # SQLite: Filter in Python
            rides = Ride.objects.filter(user=self.request.user)
            filtered_rides = []
            for ride in rides:
                try:
                    meta_data = json.loads(ride.ExternalMetaData)
                    if not key and meta_data.get('account_id') == int(account_id):
                        filtered_rides.append(ride)
                    elif meta_data.get('key') == key:
                        filtered_rides.append(ride)      
                except json.JSONDecodeError:
                    continue  # Handle or log JSON decode error if needed
            queryset =  filtered_rides
            # TODO: Update key seletion sql server
        elif 'mssql' in connection.settings_dict['ENGINE']:
            # SQL Server: Filter using RawSQL
            account_id_str = str(account_id)
            rides = Ride.objects.annotate(
                account_id_json=RawSQL("JSON_VALUE(ExternalMetaData, '$.account_id')", ())
            ).filter(account_id_json=account_id_str,user=self.request.user)
            queryset = rides
        else:
            # Add support for other databases as needed
            raise NotImplementedError("Database backend not supported")


        Country = self.request.query_params.get('Country')
        DistrictRegion = self.request.query_params.get('DistrictRegion')
        CityMunicipality = self.request.query_params.get('CityMunicipality')
        ServiceCategory = self.request.query_params.get('ServiceCategory')
        RideType = self.request.query_params.get('RideType')
        Blocked = self.request.query_params.get('Blocked')
        Canceled = self.request.query_params.get('Canceled')
        Deleted = self.request.query_params.get('Deleted')
        NotAvailable = self.request.query_params.get('NotAvailable')
        
        #Todo: Error ID --> Query by ID --> record
        if Country is not None:
            queryset = [ record for record in  queryset if record.Country == Country ]
        if DistrictRegion is not None:
            queryset = [ record for record in  queryset if record.DistrictRegion == DistrictRegion ]
        if CityMunicipality is not None:
            queryset = [ record for record in  queryset if record.CityMunicipality == CityMunicipality ]
        if ServiceCategory is not None:
            queryset = [ record for record in  queryset if record.ServiceCategory == ServiceCategory ]
        if RideType is not None:
            queryset = queryset.filter(RideType=RideType)
        if Blocked is not None:
            if Blocked == '1':
                queryset = [ record for record in  queryset if record.Blocked == True ]
            elif Blocked == '0':
                queryset = [ record for record in  queryset if record.Blocked == False ]
        if Canceled is not None:
            if Canceled == '1':
                queryset = [ record for record in  queryset if record.Canceled == True ]
            elif Canceled == '0':
                queryset = [ record for record in  queryset if record.Canceled == False ]
        if Deleted is not None:
            if Deleted == '1':
                queryset = [ record for record in  queryset if record.Deleted == True ]
            elif Deleted == '0':
                queryset = [ record for record in  queryset if record.Deleted == False ]
        if NotAvailable is not None:
            if NotAvailable == '1':
                queryset = [ record for record in  queryset if record.NotAvailable == True ]
            elif NotAvailable == '0':
                queryset = [ record for record in  queryset if record.NotAvailable == False ]
        
        return queryset
 
# Booking: ViewSets define the view behavior.
class bookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling API requests related to bookings of rides.
    
    Supports standard CRUD operations with token authentication and additional custom actions
    for specific use cases like canceling and deleting bookings.
    

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return bookingCreateSerializer
        return bookingSerializer

    def createTEST(self, request, *args, **kwargs):
        """
        Handles the creation of a new booking instance.

        Validates the serializer, assigns stock items, calculates total prices, 
        and initializes the booking-related attributes. If validation
        fails or certain conditions are not met, an appropriate response
        is returned. An email notification is sent upon successful creation.
        """
        # Serializer validation and booking initialization logic
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=False):
            return Response({"Fail": "blablal"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        
        pk = int(serializer.data['pk'])
        booking = Booking.objects.get(pk=pk)
        Mkt =  ContrSectionRideMkt.objects.get(pk=booking.Stock_Id)
        ride_booked = booking.ride

        
        
        Duration = RideDuration.objects.values_list('Token', flat = True)
        Equipement = equipment.objects.values_list('Token', flat = True)
        Sound = sound.objects.values_list('Token', flat = True)
        Image = image.objects.values_list('Token', flat = True)
        Localwifi = localwifi.objects.values_list('Token', flat = True)

        # Assorted logic related to ride equipment, expectations, and settings
        for item in json.loads(Mkt.setting):
            if item in Duration:
                booking.ExpectDuration = RideDuration.objects.get(Token = item)
            elif item in Equipement:
                booking.Equipment = equipment.objects.get(Token = item)
            elif item in Sound:
                booking.Sound = sound.objects.get(Token = item)
            elif item in Image:
                booking.Image = image.objects.get(Token = item)
            elif item in Localwifi:
                booking.localwifi = localwifi.objects.get(Token = item)
            else:
                booking.ErrorMessages ="Fail: Seetings " + "item"
                booking.save()
                return Response({"Fail": "Seetings"}, status=status.HTTP_400_BAD_REQUEST)
  
        booking.SelectStock = True
        # Calculation of total price based on market data and assignment of expected services
        
        booking.TotalPrice = Mkt.TotalPrice

        # Stripe: payment link

        # Ride Stock: Kit

        # Generate: Surogate Dashboard

        # Generate: Teams meeting

        booking.save()

        # Sending an email notification about the booking registration
        
        #if CountryID:
        #    comm = commchannel.objects.filter(Country = CountryID)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET

        message = render_to_string('emails_backoffice/booking_ride.html', {
            'UserID': request.user.pk,
            'User': request.user.username,
            'RideID': ride_booked.pk,
            'BookingID': booking.pk,  
            'Title': ride_booked.ServiceTitle, 
            'RideDate': ride_booked.RideDate,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(pk)+'/change/', 
            'STATUS': 'Registred',
        })
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support:  Ride booked',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        # Successful response upon creating booking
        return Response({"Success": 1, "booked": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    # Custom action: canceling a booking
    @action(detail=True, methods=['get'], name='Cancel ride')
    def cancel(self, request, pk=None):
        """
        Cancels a booking if it hasn't started yet, updates booking status, and sends notification.
        """
        booking = self.get_object()
        if not booking.RideStarted:
            # Implementation of ride cancellation logic, including email notification
        
            booking.Canceled = True
            booking.save()

            # Request streaming link 
            #booking_pk = booking.pk
            #start_time = "2024-10-18T17:00:00Z"
            #end_time = "2024-10-18T18:00:00Z"
            #book_room_async(booking_pk, start_time, end_time)



            #if self.Country:
            #    comm = commchannel.objects.filter(Country = self.ride.Country)
            #    mail_backoffice = comm.mail_ride
            #else:
            mail_backoffice = settings.EMAILMARKET
            
            message = render_to_string('emails_backoffice/booking_status_changed.html', {
                'UserID': booking.user.pk,
                'User': booking.user.username,
                'RideID': booking.ride.pk if booking.ride else None,  
                'Title': booking.ServiceTitle,
                'BookedID': booking.pk,
                'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
                'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
                'STATUS': 'cancel',
            })
            
            # Define email message
            email_message = {
                "message": {
                    "subject": 'Support: Booking Canceled',
                    "body": {
                        "contentType": "Text",
                        "content": message
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address":  mail_backoffice
                            }
                        }
                    ]
                }
            }
            
            EmailThread(email_message).start()

            return Response({'status': 'OK','booking': core_serializers.serialize('json', [booking,])})
        return Response({'status': 'ERROR','Error':'102','Message': 'The ride started','booking':  core_serializers.serialize('json', [booking,])})
    
    # Custom action: deleting a booking
    @action(detail=True, methods=['get'], name='Remove ride booking')
    def delete(self, request, pk=None):
        """
        Deletes a booking based on cancellation status, updates booking status, and sends notification.
        """
        booking = self.get_object()
        if booking.Canceled:
            # Implementation of booking deletion logic, including email notification
            booking.Deleted = True # add condition
            booking.save()

            #if self.Country:
            #    comm = commchannel.objects.filter(Country = self.ride.Country)
            #    mail_backoffice = comm.mail_ride
            #else:
            mail_backoffice = settings.EMAILMARKET
            
            message = render_to_string('emails_backoffice/booking_status_changed.html', {
                'UserID': booking.user.pk,
                'User': booking.user.username,
                'RideID': booking.ride.pk if booking.ride else None,  
                'Title': booking.ServiceTitle,
                'BookedID': booking.pk,
                'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
                'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
                'STATUS': 'delete',
            })
            
            # Define email message
            email_message = {
                "message": {
                    "subject": 'Support: Ride booking Deleted',
                    "body": {
                        "contentType": "Text",
                        "content": message
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address":  mail_backoffice
                            }
                        }
                    ]
                }
            }
            
            EmailThread(email_message).start()

            return Response({'status': 'OK','booking':  core_serializers.serialize('json', [booking,])})
        return Response({'status': 'ERROR','Error':'101','Message': 'Only canceled rides can be deleted.','booking':  core_serializers.serialize('json', [booking,])})

    # Custom action: paying ride extra costs
    @action(detail=True, methods=['get'], name='Ride extras')
    def extra_costs (self, request, pk=None):
        """
        Handles additional costs for a booking.
        Updates booking details to reflect extra costs and sends a notification.
        """
        # Addition of extra costs to the booking
        booking = self.get_object()
        ExtraPrice = request.query_params.get('ExtraPrice')
        booking.ExtraPrice = ExtraPrice
        booking.save()
        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
            'STATUS': 'extra_costs',
        })
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride extra costs added',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK','booking': core_serializers.serialize('json', [booking,])})

    # Custom action: disputing a ride
    @action(detail=True, methods=['get'], name='Dispute Ride')
    def dispute (self, request, pk=None):
        """
        Marks a ride as disputed within the booking.
        Updates booking details to reflect dispute status and sends a notification.
        """
        # Implementation of booking dispute marking logic
        booking = self.get_object()
        booking.Disputed = True
        booking.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
            'STATUS': 'dispute',
        })
        
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride distputed',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'Ride disputed','booking':  core_serializers.serialize('json', [booking,])})

    def send(self, request, pk=None):
        """Client classification """
        message = request.query_params.get('message')
        booking = self.get_object()
        board = MessageBoard()
        board.user = booking.user
        board.SendByClient = True
        board.Text = message
        board.booking = booking

        board.save()

        return Response({'status': 'OK','message': core_serializers.serialize('json', [board,])})  

    @action(detail=True, methods=['get'], name='Request payment link')
    def paymentlink(self, request, pk=None):
        """payment link """
        booking = self.get_object()
        booking.GeneratePaymentLink = True # reques payment link
        booking.PaymentLink = 'xxx999xxx'
        booking.save()
        
        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
            'STATUS': 'paymentlink', 
        })

        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride booking payment link',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK','booking': core_serializers.serialize('json', [booking,])})

    @action(detail=True, methods=['get'], name='Request payment link')
    def dashoards(self, request, pk=None):
        """dashoards generation """
        booking = self.get_object()
        booking.APIrequiresDashboardURL = True # reques payment link
        booking.DashboardClientURL = 'xxx999xxx'
        booking.ClientKey = '1223'
        booking.DashboardSurrogateURL = 'xxx9888xxx'
        booking.SurrogateKey = 'xxx999xxx'
        booking.save()

        
        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
            'STATUS': 'dashoards', 
        })

       
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride dashboards',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK','booking': core_serializers.serialize('json', [booking,])})

    @action(detail=True, methods=['get'], name='Client classification')
    def client_classification (self, request, pk=None):
        """Client classification """
        rank = request.query_params.get('ClientRank')
        booking = self.get_object()
        booking.ClientRank = rating.objects.get(pk=rank)
        booking.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
            'STATUS': 'client_classification',
        })
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride Client classification',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK','booking': core_serializers.serialize('json', [booking,])})  

    @action(detail=True, methods=['get'], name='Surrogate classification')
    def surrogate_classification (self, request, pk=None):
        """Client classification """
        booking = self.get_object()
        rank = request.query_params.get('AgentRank')
        booking.AgentRank =  rating.objects.get(pk=rank)
        booking.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
            'STATUS': 'surrogate_classification',
        })
                
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride surrogate classification',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK','booking':  core_serializers.serialize('json', [booking,])})

    @action(detail=True, methods=['get'], name='Start ride')
    def ride_start(self, request, pk=None):
        """Start Ride """
        booking = self.get_object()
        booking.RideStarted = True
        booking.RideStartDate = timezone.now()
        booking.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
            'STATUS': 'Close',
        })
        
                        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride Start',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK', 'booking': core_serializers.serialize('json', [booking,])})
    
    @action(detail=True, methods=['get'], name='End ride')
    def ride_end(self, request, pk=None):
        """End Ride """
        booking = self.get_object()
        booking.RideEnded = True
        booking.RideEndDate = timezone.now()
        booking.save()


        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(booking.pk)+'/change/',
            'STATUS': 'ride_end',
        })
        
                        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride End',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK', 'booking': core_serializers.serialize('json', [booking,])})
    
    @action(detail=True, methods=['get'], name='Close ride')
    def close(self, request, pk=None):
        """Cancel Ride """
        booking = self.get_object()
        booking.closed = True
        booking.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/booking_status_changed.html', {
            'UserID': booking.user.pk,
            'User': booking.user.username,
            'RideID': booking.ride.pk if booking.ride else None,  
            'RideID': booking.ride.pk if booking.ride else None,  
            'Title': booking.ServiceTitle,
            'BookedID': booking.pk,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.ride.pk)+'/change/' if booking.ride else None,
            'BookingURL': settings.DOMAIN+'/admin/rides/ride/'+str(booking.pk)+'/change/',
            'STATUS': 'close',
        })
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Support: Ride closed',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'OK', 'booking': core_serializers.serialize('json', [booking,])})
   

    def get_queryset(self):
        """
        Customizes the queryset based on various filter parameters provided in the request.
        
        Filters the bookings by ride ID, client selection, and different status flags such as
        completed, canceled, selected, requisites satisfied, expired, disputed, error, and blocked.
        """
        queryset = Booking.objects.filter(user=self.request.user, closed=False)
        ride = self.request.query_params.get('ride')
        SelectStock = self.request.query_params.get('select-agent')
        Completed = self.request.query_params.get('completed')
        Canceled = self.request.query_params.get('canceled')
        StockSelected = self.request.query_params.get('agent-selected')
        RequisitedSatisfied = self.request.query_params.get('requisits-satisfied')
        Expired = self.request.query_params.get('expired')
        Disputed = self.request.query_params.get('disputed')
        Error = self.request.query_params.get('error')
        Blocked = self.request.query_params.get('blocked')
        Deleted = self.request.query_params.get('deleted')
        if ride is not None:
            queryset = queryset.filter(ride=ride)
        if SelectStock is not None:
            if SelectAgent == '1':
                queryset = queryset.filter(SelectStock=True)
            elif SelectAgent == '0':
                queryset = queryset.filter(SelectStock=False)
        if Completed is not None:
            if Completed == '1':
                queryset = queryset.filter(Completed=True)
            elif Completed == '0':
                queryset = queryset.filter(Completed=False)
        if Canceled is not None:
            if Canceled == '1':
                queryset = queryset.filter(Canceled=True) 
            elif Canceled == '0':
                queryset = queryset.filter(Canceled=False) 
        if StockSelected is not None:
            if AgentSelected == '1':
                queryset = queryset.filter(StockSelected=True)
            elif AgentSelected == '0':
                queryset = queryset.filter(StockSelected=False) 
        if RequisitedSatisfied is not None:
            if RequisitedSatisfied == '1':
                queryset = queryset.filter(RequisitsSatisfied=True) 
            elif RequisitedSatisfied == '0':
                queryset = queryset.filter(RequisitsSatisfied=False)
        if Expired is not None:
            if Expired == '1':
                queryset = queryset.filter(Expired=True)
            elif Expired == '0':
                queryset = queryset.filter(Expired=False) 
        if Error is not None:
            if Error == '1':
                queryset = queryset.filter(Error=True) 
            elif Error == '0':
                queryset = queryset.filter(Error=False) 
        if Disputed is not None:
            if Disputed == '1':
                queryset = queryset.filter(Disputed=True) 
            elif Disputed == '0':
                queryset = queryset.filter(Disputed=False)
        if Blocked is not None:
            if Blocked == '1':
                queryset = queryset.filter(Blocked=True)
            elif Blocked == '0':
                queryset = queryset.filter(Blocked=False)
        if Deleted is not None:
            if Deleted == '1':
                queryset = queryset.filter(Deleted=True)     
            elif Deleted == '0':
                queryset = queryset.filter(Deleted=False)
        return queryset


# Ride: ViewSets define the view behavior.
class stockViewSet(viewsets.ModelViewSet): 
    """
    A viewset for handling API requests related to stock items in contract ride markets.

    It provides standard CRUD operations and custom actions for selecting and unselecting stock items.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ContrSectionRideMkt.objects.all()
    serializer_class = stockSerializer

    @action(detail=True, methods=['get'], name='select stock item')
    def selected (self, request, pk=None):
        """
        Marks the stock item as selected and sends an email notification.

        This custom action updates the `Selected` status of a given stock item to `True` 
        and triggers an email to notify relevant parties of the change in status.
        """
        item = self.get_object()
        item.Selected = True
        item.save()

        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        
        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/stock_status_changed.html', {
            'UserID': item.user.pk,
            'User': item.user.username,
            'RideID': item.Ride.ride.pk,  
            'Title': item.Ride.ride.ServiceTitle,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(item.Ride.ride.pk)+'/change/',
            'BookedID': item.Ride.pk, 
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(item.Ride.pk)+'/change/',
            'ItemID': item.pk,
            'ItemURL': settings.DOMAIN+'/admin/rides/contrsectionridemkt/'+str(item.pk)+'/change/',
            'STATUS': 'selected',
        })
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'SSupport: Stock selected',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()

        return Response({'status': 'Selected stock item', 'item':core_serializers.serialize('json', [item,])})

    @action(detail=True, methods=['get'], name='Unselect stock item')
    def unselected (self, request, pk=None):
        """
        Marks the stock item as unselected and sends an email notification.

        This custom action updates the `Selected` status of a given stock item to `False`
        and triggers an email to notify relevant parties that the item is no longer selected.
        """
        item = self.get_object()
        item.Selected = False
        item.save()

        mail_backoffice = settings.EMAILMARKET
        
        message = render_to_string('emails_backoffice/stock_status_changed.html', {
            'UserID': item.user.pk,
            'User': item.user.username,
            'RideID': item.Ride.ride.pk,  
            'Title': item.Ride.ride.ServiceTitle,
            'RideURL': settings.DOMAIN+'/admin/rides/ride/'+str(item.Ride.ride.pk)+'/change/',
            'BookedID': item.Ride.pk, 
            'BookingURL': settings.DOMAIN+'/admin/rides/booking/'+str(item.Ride.pk)+'/change/',
            'ItemID': item.pk,
            'ItemURL': settings.DOMAIN+'/admin/rides/contrsectionridemkt/'+str(item.pk)+'/change/',
            'STATUS': 'unselected',
        })
        
        
        # Define email message
        email_message = {
            "message": {
                "subject": 'Stock unselected',
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address":  mail_backoffice
                        }
                    }
                ]
            }
        }
        
        EmailThread(email_message).start()
        
        return Response({'status': 'UnSelected stock item', 'item':core_serializers.serialize('json', [item,])})

    def get_queryset(self):
        """
        Customizes the queryset to display stock items related to the current user and optional booking parameter.
        """
        queryset = ContrSectionRideMkt.objects.filter(user=self.request.user)
        ride = self.request.query_params.get('booking')
       
        if ride is not None:
            queryset = queryset.filter(Ride=ride)

        return queryset

# Ride: ViewSets define the view behavior.
class messageViewSet(viewsets.ModelViewSet): 
    """
    A viewset for handling API requests related to messaging on the message board.

    It provides standard CRUD operations and custom actions for marking messages as read, deleted, or abusive.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = MessageBoard.objects.all()
    serializer_class = MessageBoardSerializer

    def get_queryset(self):
        """
        Customizes the queryset to display messages related to the current user and optional booking parameter.
        """
        # Filter the queryset based on the current user and booking query parameter
        
        queryset = MessageBoard.objects.filter(user=self.request.user)
        ride = self.request.query_params.get('booking')
        if ride is not None:
            queryset = queryset.filter(booking=ride)

        return queryset
    
    @action(detail=True, methods=['get'], name='Close ride')
    def readed(self, request, pk=None):
        """
        Marks a message as read.
        
        This custom action updates the `Read` status of the message.
        """
        board = self.get_object()
        if board.SendByClient:
            board.Read = True
            board.save()

        return Response({'status': 'OK', 'message': core_serializers.serialize('json', [board,])})
   
    @action(detail=True, methods=['get'], name='Delete message')
    def delete(self, request, pk=None):
        """
        Deletes a message from the message board.

        This custom action sets the `deleted` flag for the message, marking it as removed by the client.
        """
        board = self.get_object()
        if board.SendByClient:
            board.deleted = True
            board.save()

        return Response({'status': 'OK', 'message': 'Deleted'})

    @action(detail=True, methods=['get'], name='Report as abusive')
    def abuse(self, request, pk=None):
        """
        Reports a message as abusive.
        
        This custom action marks the message as abusive, updating its `Abuse` status.
        """
        board = self.get_object()
        if not board.SendByClient:
            board.Read = True
            board.save()

        return Response({'status': 'OK', 'message': core_serializers.serialize('json', [board,])})
    