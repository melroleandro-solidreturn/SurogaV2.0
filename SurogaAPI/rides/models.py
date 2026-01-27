"""
Rides App Models - Suroga API

This module contains the Django models for the 'rides' application within the Suroga API. These models define the essential
entities and concepts for the rides management system, such as Bookings, Rides, Communication Logs, Payment Logs, and
other related features.

Each model represents a table in the database and includes fields that correspond to the different columns within that table.
The models are equipped with attributes and methods to handle business logic, data integrity, and relationships between
different entities.

Usage:
    Instances of these models can be created, retrieved, updated, and deleted through Django's Object-Relational Mapping (ORM)
    layer, providing an abstraction over the database operations. The models are also used in Django's admin interface,
    views, and other parts of the application where ride-related data is needed.

References:
    - Django model reference: https://docs.djangoproject.com/en/4.0/ref/models/
    - Django ORM documentation: https://docs.djangoproject.com/en/4.0/topics/db/

The file structure and Django model conventions should be maintained to keep the models aligned with best practices
and the overall architecture of the Suroga API project.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""
import datetime
import hashlib

from django.db import models, IntegrityError
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.contrib.auth import get_user_model
User = get_user_model()

from core.models import equipment, country, districtregion, citymunicipality, RideDuration, image, sound, localwifi, publicevent
#from  commchannel  

from kit.models import kitstock, kittype 
from supplier.models import contractsection, profilerepresentative, commtype
#from rides.models import rating, RideDuration, ServiceCategory,  ridetype, Ride, Booking, ContrSectionRideMkt, mettinglog

from core.extras import EmailThread
from django.conf import settings

# Create your models here.

class rating(models.Model):
    """
    Model representing a rating system used for grading rides, users, clients, and services.
    
    Attributes:
        Name: A label representing the rating classification (e.g., 'Excellent', 'Poor').
        Value: A numerical value associated with the rating (default is 2).
    """
    Name = models.CharField(max_length=20,  blank=False, help_text = "Classification")
    value = models.IntegerField(default=2, help_text= "Rating value")
    class Meta:
        verbose_name_plural = "Ratings"
    def __str__(self):
        return self.Name

class ServiceCategory(models.Model):
    """
    Model representing different categories of services offered.
    
    Attributes:
        Name: The name of the service category (e.g., 'Transportation', 'Delivery').
    """
    Name = models.CharField(max_length=100, unique=True, blank=False, help_text = "Service Category")
    class Meta:
        verbose_name_plural = "Service Categories"
    def __str__(self):
        return self.Name
        
class ridetype(models.Model):
    """
    Model representing different types of rides.
    
    Attributes:
        Name: The name of the ride type (e.g., 'Standard', 'VIP').
    """
    Name = models.CharField(max_length=100, unique=True, blank=False, help_text = "Ride type")
    class Meta:
        verbose_name_plural = "Ride Types"
    def __str__(self):
        return self.Name

class Ride(models.Model):
    """
    Model representing the details of a ride service.
    
    Attributes:
        (Several attributes such as user identification, service location, time fields, service descriptions, requisites, etc.
         Below is an example subset of these attributes for brevity.)
        User: A ForeignKey linking to the user who created the ride.
        ExternalMetaData: A TextField to store metadata added by the application.
        InternalMetaData: A TextField storing internal API metadata.
        PayedAtRegistration: A BooleanField indicating if payment was made upon registration.
        RideDate: A DateTimeField storing the date and time of the ride.
        ServiceTitle: A CharField for the title of the ride service.
        Description: A TextField describing the service.
        RegistrationDate: A DateTimeField storing when the ride was registered.
        HashKey: A CharField storing a unique hash key for the service identification.
    """
    # User identification
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name='user_service')    
    ExternalMetaData = models.TextField(max_length=1000, blank=True, help_text = "APP metadata")
    InternalMetaData = models.TextField(max_length=1000, blank=True, help_text = "API metadata")
    PayedAtRegistration =  models.BooleanField(default=False, help_text = "Payment is made at the ride registration.")  
    
    # Service Localion
    Country = models.CharField(max_length=20, blank=True, help_text = "Country") 
    DistrictRegion = models.CharField(max_length=20, blank=True, help_text = "District/Region") 
    CityMunicipality = models.CharField(max_length=20, blank=True, help_text = "City/Municipality") 
    StreetName = models.CharField(max_length=100, blank=True, help_text = "Street name")
    StreetNumber = models.CharField(max_length=10, blank=True, help_text = "Street number")
    Floor = models.CharField(max_length=10, blank=True, help_text = "Floor")
    
    ZipCode = models.CharField(max_length=100, blank=True, help_text = "Zip Code part 1")
    #ZipCodeP2 = models.CharField(max_length=100, blank=True, help_text = "Zip Code part 2")
    GPS_latitude = models.DecimalField(max_digits=11, decimal_places=7,default=0, help_text = "location coordinates") 
    GPS_longitude = models.DecimalField(max_digits=11, decimal_places=7,default=0, help_text = "location coordinates") 
    Zoom_map = models.IntegerField(default=15, help_text = "Google maps zoom")
    GooglePlaceID = models.CharField(max_length=30, blank=True, editable=False, help_text = "Google place ID.")
    
    # time field
    #Time = models.TimeField(default=timezone.now, blank=True, help_text = "Ride time of the day.")
    
    # Service description
    RideDate  = models.DateTimeField(default=timezone.now,  blank=True, help_text = "Ride time and date.") 
    
    Equipment = models.ForeignKey(equipment, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Equipment used")
    PublicEvent = models.ForeignKey(publicevent, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Ride type") 
    LocalWifi = models.ForeignKey(localwifi, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Ride type") 
    Sound = models.ForeignKey(sound, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Ride type") 
    Image = models.ForeignKey(image, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Ride type")   
    ServiceTitle = models.CharField(max_length=400, editable=True, blank=True, help_text = "Service title")
    Description = models.TextField(max_length=1000, blank=True, help_text = "Service Description") 
    ExpectDuration = models.ForeignKey(RideDuration, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Expected service duration.") 
    
    RideType =  models.ForeignKey(ridetype, on_delete=models.SET_NULL, null=True, blank=True, default=1, help_text = "Ride Type") #models.CharField(default='', max_length=20, blank=True, help_text = "Ride Type") 
    ServiceCategory =  models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True,default=1, help_text = "Service Category") #models.CharField(default='', max_length=20, blank=True, help_text = "Service Category") 
    
    #configuration
    RegistrationDate = models.DateTimeField(default=timezone.now, editable=False, help_text = "Date of this registration.")
    GeneratePaymentLink = models.BooleanField(default=False, help_text = "True if API requires payment link") 
    PaymentLink = models.CharField(max_length=100, blank=True, help_text = "Link in Stripe to use for payment.")  
    PaymentCODE = models.CharField(max_length=100, blank=True, help_text = "Payment proof code.") 

    #Status
    NotAvailable = models.BooleanField(default=False, help_text = "Servide not available by SurooAPI") 
    Blocked = models.BooleanField(default=False, help_text = "Ride blocked by SurooAPI") 
    Canceled = models.BooleanField(default=False, help_text = "Service canceled via API") 
    Deleted = models.BooleanField(default=False, help_text = "Service deleted via API.") 
    Closed = models.BooleanField(default=False, help_text = "Service closed via API.") 
    
    #Identification
    HashKey = models.CharField(max_length=30, blank=True, help_text = "Service hash key.") 
    Request_Id = models.CharField(max_length=20, blank=True, editable=False, help_text = "API request ID")

    #Requisits
    Requisits = models.CharField(default='', max_length=1000, blank=True, editable=True, help_text = "Service Requisits") 



    class Meta:
        verbose_name_plural = "Rides Registered"
    
    def __str__(self):
        return self.ServiceTitle  # May vary depending on what identifies a ride instance best
            

    def save(self,force_insert=False, force_update=False, using=None):
        # Custom save method to include business logic
        if not self.HashKey:
            code = f"{self.pk}{datetime.date.today()}{datetime.datetime.today()}"
            self.HashKey = hashlib.sha1(code.encode()).hexdigest()[:30] 
        try:
            return  super(Ride, self).save()
        except Exception as exc:
            return exc 

class Booking(models.Model):
    """
    Model representing a booking made for a ride service.

    Attributes:
        user: A ForeignKey to the User model, representing the user associated with the booking.
        ExternalMetaData: Stores metadata provided by the app for the booking.
        InternalMetaData: Stores metadata used by the API for the booking.
        ride: A ForeignKey to the Ride model, linking a booking with the ride being booked.
        RideDate: A DateTimeField to specify the date for the appointment/booking.
        Sound: A ForeignKey to the sound model for potential sound requirements for the ride.
        Image: A ForeignKey to the image model for potential video requirements for the ride.
        Equipment: A ForeignKey to the equipment model for required equipment for the ride.
        localwifi: A ForeignKey to the localwifi model for required local wifi details.
        publicevent: A ForeignKey to the publicevent model for potential public event details.
        APIrequiresMettingURL: Indicates whether a meeting URL is required to be sent to the API.
        MeetingURL: Stores the meeting link if necessary for the booking.
        MeetingPasswd: Stores the meeting password or pin if necessary.
        RegistrationDate: Records when the booking was made, auto-set to the current time.
        Blocked: Indicates if a ride is blocked.
        Canceled: Indicates if the ride is canceled via the API.
        Deleted: Indicates if the ride is deleted via the API.
        ServiceTitle: Stores the title of the service being offered.
        Description: Provides a description for the service.
        ExpectDuration: A ForeignKey to the RideDuration model for expected service duration.
        FinalDuration: Stores the final distance to go or the duration it took.
        ExtraPrice: An additional cost for the service.
        SelectStock: Indicates if stock must be selected for the booking.
        Completed: Indicates if the service is selected as completed.
        StockSelected: Indicates if the stock was selected for the service.
        CanceledAgent: Indicates if the ride was canceled by the surrogate.
        RequisitsSatisfied: Indicates whether the requisites were satisfied for the ride.
        Expired: Indicates if the selection for the service has expired.
        Error: Indicates if there was an error in the selection process.
        Disputed: Indicates if the ride is in dispute.
        InvitationSend: Indicates if an invitation was sent to the surrogate.
        InvitationAccepted: Indicates if the surrogate has accepted the invitation.
        closed: Indicates if the service was completed.
        SystemInfo: Stores system information in JSON format.
        ErrorMessages: Records any error message that may have occurred.
        GeneratePaymentLink: Indicates if a payment link generation is needed.
        PaymentLink: Stores the payment link for the service if needed.
        PaymentCODE: Stores the payment proof code.

        # Fields for Dashboard links, Rankings, Ride info, and Stock info are also included.
    """
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name='Booking_service')    
    ExternalMetaData = models.TextField(max_length=1000, blank=True, help_text = "APP metadata")
    InternalMetaData = models.TextField(max_length=1000, blank=True, help_text = "API metadata")

    # Ride registration
    ride = models.ForeignKey(Ride,on_delete=models.SET_NULL, null=True, blank=True, related_name='Booking_booking')    
    ServiceTitle = models.CharField(max_length=400, editable=True, blank=True, help_text = "Service title")
    Description = models.TextField(max_length=1000, blank=True, help_text = "Service Description") 
    
    RideType =  models.ForeignKey(ridetype, on_delete=models.SET_NULL, null=True, blank=True, default=1, help_text = "Ride Type") #models.CharField(default='', max_length=20, blank=True, help_text = "Ride Type") 
    ServiceCategory =  models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, default=1, help_text = "Service Category") #models.CharField(default='', max_length=20, blank=True, help_text = "Service Category") 
    
    
    # Service Localion
    Country = models.CharField(max_length=20, blank=True, help_text = "Country") 
    DistrictRegion = models.CharField(max_length=20, blank=True, help_text = "District/Region") 
    CityMunicipality = models.CharField(max_length=20, blank=True, help_text = "City/Municipality") 
    StreetName = models.CharField(max_length=100, blank=True, help_text = "Street name")
    StreetNumber = models.CharField(max_length=10, blank=True, help_text = "Street number")
    Floor = models.CharField(max_length=10, blank=True, help_text = "Floor")
    
    ZipCode = models.CharField(max_length=100, blank=True, help_text = "Zip Code part 1")
    #ZipCodeP2 = models.CharField(max_length=100, blank=True, help_text = "Zip Code part 2")
    GPS_latitude = models.DecimalField(max_digits=11, decimal_places=7,default=0, help_text = "location coordinates") 
    GPS_longitude = models.DecimalField(max_digits=11, decimal_places=7,default=0, help_text = "location coordinates") 
    Zoom_map = models.IntegerField(default=15, help_text = "Google maps zoom")
    GooglePlaceID = models.CharField(max_length=30, blank=True, editable=False, help_text = "Google place ID.")
    

    # Ride date
    RideDate  = models.DateTimeField(default=timezone.now,  blank=False, help_text = "Appointment date.") 
    Sound = models.ForeignKey(sound, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Sound requisits") 
    Image = models.ForeignKey(image, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Video requisits")   
    Equipment = models.ForeignKey(equipment, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Required equipment", related_name='service_equipment') 
    LocalWifi = models.ForeignKey(localwifi, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Local wifi", related_name='service_wifi') 
    PublicEvent = models.ForeignKey(publicevent, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Public event", related_name='service_public') 
    
    
    # Meeting config
    APIrequiresMettingURL = models.BooleanField(default=True, help_text = "True if meeting URL must be sent to API")
    MeetingURL = models.CharField(max_length=100, editable=True, blank=True, help_text = "The meeting link")
    MeetingPasswd = models.CharField(max_length=100, editable=True, blank=True, help_text = "The meeting password/pin")
    
    RegistrationDate = models.DateTimeField(default=timezone.now, editable=False, help_text = "Date of this registration.")

    # Satus
    Blocked = models.BooleanField(default=False, help_text = "Ride blocked by Suroga.") 
    Canceled = models.BooleanField(default=False, help_text = "Ride canceled via API") 
    Deleted = models.BooleanField(default=False, help_text = "Ride deleted via API") 

    # Service description
    #ServiceTitle = models.CharField(max_length=400, editable=True, blank=True, help_text = "Service title")
    #Description = models.TextField(max_length=1000, blank=True, help_text = "Service Description") 
    ExpectDuration = models.ForeignKey(RideDuration, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Expected service duration.") 
    FinalDuration = models.DecimalField(max_digits=5, decimal_places=2,default=0, help_text = "Distance to go in doing the service.")
    ExtraPrice = models.DecimalField(max_digits=5, decimal_places=2,default=0.0, help_text = "Extra price.")
    
    # configuration
    SelectStock = models.BooleanField(default=False, help_text = "True if stock must be selected") 
    Completed = models.BooleanField(default=False, help_text = "True if service selected") 
    StockSelected = models.BooleanField(default=False, help_text = "True if stock was selected") 
    CanceledAgent = models.BooleanField(default=False, help_text = "True if ride canceled by surrogate") 
    RequisitsSatisfied = models.BooleanField(default=False, help_text = "True if ride riquisites were satisfied") 
    Expired = models.BooleanField(default=False, help_text = "True if selection expired") 
    Error = models.BooleanField(default=False, help_text = "True if error on seelction process") 
    Disputed = models.BooleanField(default=False, help_text = "True if ride is in dispute") 
    InvitationSend = models.BooleanField(default=False, help_text = "True if invitation was sent to surrogate")
    InvitationAccepted = models.BooleanField(default=False, help_text = "True if invitation was accepted by surrogate")
    closed = models.BooleanField(default=False, help_text = "True if service was completed")

    # System status
    SystemInfo = models.TextField(max_length=1000, blank=True, help_text = "JSON: System information")
    ErrorMessages = models.TextField(max_length=100, blank=True, help_text = "Error message")

    #Payment
    GeneratePaymentLink = models.BooleanField(default=False, help_text = "True if API requires payment link") 
    PaymentLink = models.CharField(max_length=100, blank=True, help_text = "Link in Stripe to use for payment.")  
    PaymentCODE = models.CharField(max_length=100, blank=True, help_text = "Payment proof code.") 

    # Dashboards
    APIrequiresDashboardURL = models.BooleanField(default=True, help_text = "True if API requires dashdoards") 
    DashboardClientURL = models.CharField(max_length=100, blank=True, editable=True, help_text = "Client dasboard on surooAPI") 
    ClientKey = models.CharField(max_length=10, blank=True, help_text = "Client Key")
    DashboardSurrogateURL = models.CharField(max_length=100, blank=True, editable=True, help_text = "Surrogate dasboard on surooAPI") 
    SurrogateKey = models.CharField(max_length=10, blank=True, help_text = "Client Key")

    # Ranking
    AgentRank = models.ForeignKey(rating, on_delete=models.CASCADE, null=True, blank=True, help_text = "Surrogate rating", related_name='booking_surrrank') 
    ClientRank = models.ForeignKey(rating, on_delete=models.CASCADE, null=True, blank=True, help_text = "Client rating", related_name='booking_clientrank') 
    SupplierARank= models.ForeignKey(rating, on_delete=models.CASCADE, null=True, blank=True, help_text = "Supplier A rating", related_name='booking_Arank') 
    SupplierBRank = models.ForeignKey(rating, on_delete=models.CASCADE, null=True, blank=True, help_text = "Supplier B rating", related_name='booking_Brank')
    SupplierCRank = models.ForeignKey(rating, on_delete=models.CASCADE, null=True, blank=True, help_text = "Supplier C rating", related_name='booking_Crank')
    SupplierDRank = models.ForeignKey(rating, on_delete=models.CASCADE, null=True, blank=True, help_text = "Supplier D rating", related_name='booking_Drank')
    SupplierERank = models.ForeignKey(rating, on_delete=models.CASCADE, null=True, blank=True, help_text = "Supplier E rating", related_name='booking_Erank')
    SupplierFRank = models.ForeignKey(rating, on_delete=models.CASCADE, null=True, blank=True, help_text = "Supplier F rating", related_name='booking_Fank')

    # Ride
    RideStarted = models.BooleanField(default=False, help_text = "Ride started.") 
    RideEnded = models.BooleanField(default=False, help_text = "Ride ended.") 
    RideStartDate = models.DateTimeField(default=timezone.now, editable=True, help_text = "Date ride start.")
    RideEndDate = models.DateTimeField(default=timezone.now, editable=True, help_text = "Date ride end.")
    
    #Identification
    HashKey = models.CharField(max_length=30, blank=True, help_text = "Service hash key.") 
    Request_Id =  models.CharField(max_length=20, blank=True, editable=False, help_text = "API request ID")
    
    #Ride Stock
    KitPack = models.ForeignKey(kitstock, on_delete=models.CASCADE, null=True, blank=True, help_text = "kit", related_name='booking_kit')
    Kit_Ref_Number=  models.CharField(max_length=15, blank=True, editable=False, help_text = "Kit Ref Number")
    Surrogate = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, help_text = "Surrogate with account", related_name='booking_agent')
    Stock_Id = models.IntegerField(default=0, help_text = "Stock Id")
    
    class Meta:
        verbose_name_plural = "Rides Booked" # The plural name for the model in the admin interface.
    
    #def __str__(self):
    #    return self.ServiceTitle  # Human-readable string representation of the model, returning the ServiceTitle.
    

    def saveTEST(self,force_insert=False, force_update=False, using=None):
        """
        Custom save method for Booking models. Upon saving, it may trigger an email to be sent
        and ensure unique hash keys are generated for identification. If there are specific country
        settings, they can be applied here as well.

        Also included is a threaded approach to send emails in the background.
        """
        
        # An email is composed and sent to a back-office email address to notify about the booking.
        
        #if self.Country:
        #    comm = commchannel.objects.filter(Country = self.ride.Country)
        #    mail_backoffice = comm.mail_ride
        #else:
        mail_backoffice = settings.EMAILMARKET

        message = render_to_string('emails_backoffice/booking_ride.html', {
            'UserID': self.user.pk,
            'User': self.user.username,
            'RideID': self.ride.pk,  
            'Title': self.ride.ServiceTitle,
            'BookingID': self.pk, 
            'RideDate': self.RideDate 
        })
        msg = EmailMessage('Support: Booking Ride',message, to=[mail_backoffice])
        
        EmailThread(msg).start()

        # Generate a unique HashKey if not already set.

        if not self.HashKey:
            data = datetime.date.today()
            time = datetime.datetime.today()
            code = str(self.pk)+str(data)+str(time)
            self.HashKey = hashlib.sha1(code.encode()).hexdigest()[:30] 
        return super(Booking, self).save()

        # Error handling for the save operation.
        try:
            return super(Booking, self).save()
        except Exception as exc:
            return exc

class ContrSectionRideMkt(models.Model):
    """
    Model representing stock in the context of a ride service market, particularly for contract sections.

    Attributes:
        Name: A name to identify a service or stock item.
        user: A ForeignKey linking to the User that is related to this stock item.
        Ride: A ForeignKey linking to a specific Ride that this stock item is associated with.
        rank: An IntegerField representing the rank or priority of the stock item.
        miss: A CharField specifying any items that are missing from the stock.
        ContractSection[A-F]: ForeignKeys linking to various `contractsection` instances.
        KitType: A ForeignKey linking to the required kit type for this stock item.
        KitRequired: A BooleanField indicating whether a kit is required.
        ContractPrice[A-F]: DecimalFields representing prices for different contract sections.
        TotalPrice: A DecimalField representing the total price for the ride.
        HashKey: A CharField that stores a unique hash key for identification.
        Selected: A BooleanField indicating whether the stock item has been selected or started.
        RequiredConfigTime: A DecimalField stating the time required for configuration.
        setting: A TextField to store JSON configuration settings for the ride.
    """
    Name = models.CharField(default="Test",max_length=50, unique=False, blank=False, help_text = "Service name")
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_user')    
    Ride = models.ForeignKey(Ride,on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='market_booking')    
    rank = models.IntegerField(default=0, help_text = "Item rank")
    miss = models.CharField(max_length=300, blank=True, help_text = "Items missing") 
    ContractSectionA = models.ForeignKey(contractsection , on_delete=models.CASCADE, null=False, blank=False, help_text = "Contract Section A", related_name='market_sectionA') 
    ContractSectionB = models.ForeignKey(contractsection, on_delete=models.CASCADE, null=True, blank=True, help_text = "Contract Section B", related_name='market_sectionB') 
    ContractSectionC = models.ForeignKey(contractsection, on_delete=models.CASCADE, null=True, blank=True, help_text = "Contract Section C", related_name='market_sectionC')
    ContractSectionD = models.ForeignKey(contractsection, on_delete=models.CASCADE, null=True, blank=True, help_text = "Contract Section D", related_name='market_sectionD')
    ContractSectionE = models.ForeignKey(contractsection, on_delete=models.CASCADE, null=True, blank=True, help_text = "Contract Section E", related_name='market_sectionE')
    ContractSectionF = models.ForeignKey(contractsection, on_delete=models.CASCADE, null=True, blank=True, help_text = "Contract Section F", related_name='market_sectionF')
    KitType = models.ForeignKey(kittype, on_delete=models.CASCADE, null=True, blank=True, help_text = "Kit required", related_name='market_kit')
    KitRequired = models.BooleanField(default=False, help_text = "Kit required") 
    ContractPriceA = models.DecimalField(max_digits=6, decimal_places=2,default=0, help_text = "Price contract A")
    ContractPriceB = models.DecimalField(max_digits=6, decimal_places=2,default=0, help_text = "Price contract B")
    ContractPriceC = models.DecimalField(max_digits=6, decimal_places=2,default=0, help_text = "Price contract C")
    ContractPriceD = models.DecimalField(max_digits=6, decimal_places=2,default=0, help_text = "Price contract D")
    ContractPriceE = models.DecimalField(max_digits=6, decimal_places=2,default=0, help_text = "Price contract E")
    ContractPriceF = models.DecimalField(max_digits=6, decimal_places=2,default=0, help_text = "Price contract F")
    TotalPrice = models.DecimalField(max_digits=6, decimal_places=2,default=0, help_text = "Total Price")
    HashKey = models.CharField(max_length=30, blank=True, editable=True, help_text = "Market hash key") 
    Selected = models.BooleanField(default=False, help_text = "Option started") 
    RequiredConfigTime  = models.DecimalField(max_digits=6, decimal_places=2,default=0, help_text = "Required config time (hours)")
    setting = models.TextField(max_length=1000, blank=True, help_text = "JSON: ride setting") 


    class Meta:
        verbose_name_plural = "Section Ride Market" # Reflects the human-readable name for the object in plural form
    

    
    def save(self,force_insert=False, force_update=False, using=None):
        """
        Overrides the default save method to generate a hash key before saving if it doesn't exist yet.

        The generated hash key is based on the current date, time, and the primary key value of the instance.
        """
        if not self.HashKey:
            # Generating the hash key based on the instance's primary key, current date, and time.
            data = datetime.date.today()
            time = datetime.datetime.today()
            code = str(self.pk)+str(data)+str(time)
            self.HashKey = hashlib.sha1(code.encode()).hexdigest()[:30] 
        
        # Attempt to save the instance using the superclass's save method

        try:
            return super(ContrSectionRideMkt, self).save()
        except Exception as exc:
            return exc


class mettinglog(models.Model):
    """
    Model for logging meeting-related actions and statuses.

    Attributes:
        Ride: A ForeignKey linking to the `Booking` with which the meeting is associated.
        ActionType: A CharField indicating the type of action in the meeting log.
        DateTime: A DateTimeField recording the date and time of the entry.
        Status: A CharField indicating the current status of the meeting.
    """
    Ride = models.ForeignKey(Booking,on_delete=models.SET_NULL, null=True, blank=True, related_name='meeting_booking')     
    ActionType = models.CharField(max_length=20, unique=True, blank=False, help_text = "Action type")
    DateTime = models.DateTimeField(default=timezone.now, editable=False, help_text = "Date")
    Satus = models.CharField(max_length=20, unique=True, blank=False, help_text = "Metting status")

    class Meta:
        verbose_name_plural = "Meeting Log" # Reflects the human-readable name for the object in plural form



class commlog(models.Model):
    """
    Model used for logging communication events related to ride services. 

    Attributes:
        POC: A reference to 'profilerepresentative', indicating the point of contact for the communication.
        Ride: A ForeignKey to the 'Booking' model - denoting which booking the communication pertains to.
        Contract: A ForeignKey to 'contractsection', showing which contract section is relevant to the communication.
        DateTime: A DateTimeField capturing the exact date and time when the communication took place.
        Message: A TextField storing the actual content of the communication message.
        Comm_Type: A ForeignKey to 'commtype', defining the type of communication that occurred.
        Attributes: A TextField to hold any additional JSON-formatted communication attributes.

    The Meta class sets the plural name for use within the Django admin site.
    """
    POC = models.ForeignKey(profilerepresentative,on_delete=models.SET_NULL, null=True, blank=True,related_name='comm_POC')   
    Ride = models.ForeignKey(Booking,on_delete=models.SET_NULL, null=True, blank=True,related_name='comm_Ride')   
    Contract = models.ForeignKey(contractsection,on_delete=models.SET_NULL,null=True, blank=True, related_name='comm_contractsection') 
    DateTime = models.DateTimeField(default=timezone.now) 
    Message = models.TextField(max_length=1000, blank=True, help_text = "Comm message") 
    Comm_Type = models.ForeignKey(commtype,on_delete=models.SET_NULL, null=True, blank=True, related_name='comm_Type') 
    Attributes = models.TextField(max_length=1000, blank=True, help_text = "JSON: comm att") 

    class Meta:
        verbose_name_plural = "Communication Logs"


class paymentlog(models.Model):
    """
    Model for recording detailed payment transaction information.

    Attributes:
        user: A ForeignKey to Django's built-in User model, associating a payment log with a specific user.
        PlantformUserType: A field specifying the type of the platform user involved in the transaction.
        OperationType: A field specifying the type of operation (e.g., deposit, withdrawal).
        SettlementDate: A DateTimeField recording when the transaction was settled.
        PaymMethodResul: A field indicating the result of the payment method transaction.
        StripTransactionID: A field storing the transaction ID from the Stripe service.
        SurooBankTransactionID: A field storing a transaction ID from Suroo's banking service.
        Ride: A ForeignKey to 'Booking' that associates the payment with a particular ride.
        Booking: Another ForeignKey to 'Booking', which might be redundant or for a different purpose (requires clarification).
        Value: A DecimalField capturing the value amount of the transaction.
        is_debit: A BooleanField indicating whether the transaction is a debit.
        RegistrationDate: A DateTimeField marking when the payment log entry was created.

    The Meta class defines the plural name for the model as it will appear in the Django admin.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default="", help_text = "payment_user") 
    PlantformUserType = models.CharField(max_length=10, unique=True, blank=False, help_text = "User type")
    OperationType = models.CharField(max_length=10, unique=True, blank=False, help_text = "Operation type")
    SettlementDate  = models.DateTimeField(default=timezone.now, editable=False, help_text = "Transation settlement date")
    PaymMethodResul = models.CharField(max_length=100, unique=True, blank=False, help_text = "Payment result")
    StripTransactionID = models.CharField(max_length=20, unique=True, blank=False, help_text = "Strip Transation ID")
    SurooBankTransactionID = models.CharField(max_length=20, unique=True, blank=False, help_text = "Bank Transation ID")  
    Ride = models.ForeignKey(Booking,on_delete=models.SET_NULL, null=True, blank=True,related_name='payment_ride')   
    Booking = models.ForeignKey(Booking,on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='payment_booking')
    Value  = models.DecimalField(max_digits=12, decimal_places=8, default=0, help_text = "Value") 
    is_debit= models.BooleanField(default=False, help_text = "True if it is a debit.")
    RegistrationDate = models.DateTimeField(default=timezone.now, editable=False, help_text = "Date of this registration.")


    class Meta:
        verbose_name_plural = "Payment log"


class bookinglog(models.Model):
    """
    Model for recording ride booking
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default="", help_text = "actionLog_user") 
    OperationType = models.CharField(max_length=10, blank=False, help_text = "Operation type")
    Ride = models.ForeignKey(Ride,on_delete=models.SET_NULL, null=True, blank=True,related_name='actionLog_ride')   
    Booking = models.ForeignKey(Booking,on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='actionLog_booking')
    RegistrationDate = models.DateTimeField(default=timezone.now, editable=False, help_text = "Date of this registration.")

    class Meta:
        verbose_name_plural = "Booking log"

class MessageBoard(models.Model):
    """
    Model for managing messages between users and related to specific bookings within the ride service.

    Attributes:
        user: A ForeignKey to Django's built-in User model, which references the user sending or receiving the message.
        booking: A ForeignKey linking a message to a booking, indicating which booking the message is pertinent to.
        SendByClient: A BooleanField that shows whether the sender of the message is the client.
        Text: A TextField that contains the body content of the message.
        Read: A BooleanField indicating whether the message has been read by the recipient.
        Date: A DateTimeField stamping the creation date and time of the message.
        deleted: A BooleanField indicating if the message was deleted by the sender.
        Abuse: A BooleanField indicating if the message was marked as abusive by the recipient.

    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default="", help_text = "API_user", related_name='message_user') 
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE, null=True, default=None, blank=True, related_name='message_booking')
    SendByClient = models.BooleanField(default=False, help_text = "True if message was sent by client")
    
    Text = models.TextField(max_length=2000, blank=True, help_text = "Message body") # Text
    Read = models.BooleanField(default=False, help_text = "Message was readed") # True if message was readed
    Date = models.DateTimeField(default=timezone.now, editable=False, help_text = "Date of this registration.")
    deleted = models.BooleanField(default=False, help_text = "deleted by sender")
    Abuse = models.BooleanField(default=False, help_text = "Classified abusive by recipient")
    
    class Meta:
        verbose_name_plural = "Message Boards"  # How the model is referred to in the admin interface in plural form

