"""
Partner App Models - Suroga API

This module defines the models for the 'partner' application within the Suroga API.
These models represent the various entities associated with partners, such as partner profiles, 
points of contact (POCs), and geographical coverage areas. The models encapsulate information concerning 
the partner's contact details, verification status for various attributes, and app related information,
as well as providing relationships to other aspects of the Suroga API like user accounts and services.

Usage: 
    - Defining the data structure for partner-related information stored in the database.
    - Use these models to interact with the database through Django's ORM in views, serializers, and other components.

Best Practices:
    - Keep model fields with clear and concise naming conventions.
    - Write detailed and comprehensive help_text for each model field for better clarity when used within the Django admin interface.
    - Maintain proper indexing and database optimization techniques for larger datasets.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""
import datetime
import hashlib

from django.db import models, IntegrityError
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.auth import get_user_model
User = get_user_model()

from core.models import country, Language
from rides.models import ServiceCategory


class profilepartner(models.Model):
    """
    Model representing a partner's profile in the partner app.

    Attributes:
        user: Reference to the user associated with the partner profile.
        Name: The full name of the partner.
        Address: Physical address of the partner.
        Zip_Code: Postal code of the partner's location.
        City: The city where the partner is located.
        Country: Reference to the country where the partner's business operations are based.
        Address_verified: Boolean field indicating whether the partner's address is verified.
        Language: The preferred language of communication for the partner.
        Telephone: Contact telephone number for the partner.
        Telephone_verified: Boolean indicating whether the partner's phone number is verified.
        ITIN: The Individual Tax Identification Number for the partner.
        ITIN_verified: Status of verification of the ITIN.
        IBAN: International Bank Account Number of the partner.
        IBAN_verified: Status of verification of the IBAN.
        HashKey: A unique hash to identify the partner.
        Registration: The timestamp when the partner was registered.
        Website: Official website URL of the partner.
        Google_play: URL to the partner's app on Google Play.
        Google_play_verified: Verification status of the app on Google Play.
        Apple_store: URL to the partner's app on the Apple Store.
        Apple_store_verified: Verification status of the app on the Apple Store.
        Stripe_ID: Stripe identification number for payment processing.
        API_activated: Status indicating whether the partner's API access is activated.
        API_test_mode: Boolean indicating if the partner is in API test mode.
        API_integration_level: Text field indicating the level of integration of the partner's API.
        APP_description: A text field to describe the partner's app in JSON format.
        APP_domain: The domain associated with the partner's app.
        APP_domain_verified: Status indicating whether the app's domain is verified.
        webwooks_suroo: URL for Suroo webhooks.
        webwooks_suroo_verified: Verification status of Suroo webhooks.
        Payment_Policy: Text field for the partner's payment policy in JSON format.
        Observation: Text field for additional observations about the partner.
        NumberRegisteredRides: The number of rides the partner has registered.
        NumberBookedRides: The number of rides the partner has booked.
        NumberCancedRides: The number of rides the partner has canceled.
        NumberCompletedRides: The number of rides the partner has completed.
        Balance: The financial balance of the partner.
        Validated_profile: Boolean indicating whether the partner's profile has been validated.
    """
    # User profile
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='partner_user')    
    
    Name = models.CharField(max_length=100, blank=True, help_text = "Partner Name") # Partner name
    Address = models.CharField(max_length=100, blank=True, help_text = "Address") # Partner address
    Zip_Code = models.CharField(max_length=100, blank=True, help_text = "Zip Code.") # Zip Code
    City = models.CharField(max_length=100, blank=True, help_text = "City") 
    Country = models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Country") 
    Address_verified  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    Language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Language") 
    Telephone = models.CharField(max_length=100, blank=True, help_text = "Business telephone.") # The contact number 
    Telephone_verified  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    ITIN = models.CharField(max_length=40, editable=True, blank=True, help_text = "Individual Tax Identification Number")    
    ITIN_verified  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    IBAN = models.CharField(max_length=40, editable=True, blank=True, help_text = "Agency IBAN")     
    IBAN_verified  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    HashKey = models.CharField(max_length=40, editable=True, blank=True, help_text = "Hash key to identity the partners agents")
    Registration = models.DateTimeField(default=timezone.now)  
    Website = models.URLField(default='',blank=True, help_text = "Partner Website. ")   
    Google_play = models.URLField(default='',blank=True, help_text = "APP in Google Play. ")   
    Google_play_verified  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    Apple_store = models.URLField(default='',blank=True, help_text = "APP in Apple Store. ")   
    Apple_store_verified  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    
    Stripe_ID = models.CharField(max_length=10, editable=True, blank=True, default='', help_text = "Partner ID")
    API_activated  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    API_test_mode  = models.BooleanField(default=True, help_text = "Test mode status TRUE=active/FALSE=inactive.") 
    API_integration_level  = models.CharField(max_length=10, editable=True, blank=True, default='', help_text = "API integration level.")
    APP_description  = models.TextField(max_length=1000, blank=True, help_text = "JSON APP description.")
    APP_domain = models.URLField(default='API calls',blank=True, help_text = "APP web domain")   
    APP_domain_verified  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    webwooks_suroo = models.URLField(default='',blank=True, help_text = "Webwook suroo alerts")   
    webwooks_suroo_verified  = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.") 
    
    Payment_Policy  = models.TextField(max_length=1000, blank=True, help_text = "JSON payment policy.")
    Observation  = models.TextField(max_length=1000, blank=True, help_text = "Observation about client.")
    
    NumberRegisteredRides = models.IntegerField(default=0, help_text = "Number registered rides")
    NumberBookedRides = models.IntegerField(default=0, help_text = "Number booked rides")
    NumberCancedRides = models.IntegerField(default=0, help_text = "Number of canced rides")
    NumberCompletedRides = models.IntegerField(default=0, help_text = "Number of completed rides")
    Balance = models.DecimalField(max_digits=7, decimal_places=2,default=0, help_text = "Balance")
    
    Validated_profile = models.BooleanField(default=False, help_text = "API status TRUE=active/FALSE=inactive.")
    
    class Meta:
            verbose_name_plural = "Partners"
        
    def __str__(self):
        """
        Returns a human-readable string representation of the partner profile.
        """
        return self.Name

    def save(self,force_insert=False, force_update=False, using=None):
        """
        Overridden save method that ensures valid data is in place before saving
        and generates a unique HashKey if it isn't provided.
        """
        self.user.Language = self.Language # for for simplification...
        # Logic for generating HashKey and saving...
        if not self.HashKey:
            data = datetime.date.today()
            time = datetime.datetime.today()
            code = str(self.pk)+str(data)+str(time)
            self.HashKey = hashlib.sha1(code.encode()).hexdigest()[:30] 
        # Error handling for the save method...    
        try:
            return super(profilepartner, self).save()
        except IntegrityError:
            return HttpResponse("ERROR: this user can not be saved...")    


class jobpoc(models.Model):
    """
    Model representing categories of Points of Contact (POC) within the partner organization.

    Attributes:
        JobCategory: A categorical description of the POC's role within the partner organization.
    """
    JobCategory = models.CharField(max_length=50, unique=True, blank=False, help_text = "POC category")
     
    class Meta:
        verbose_name_plural = "Partners POC Categories"
    def __str__(self):
        """
        Returns a string representation of the POC category.
        """
        return self.JobCategory

class partnerpoc(models.Model):
    """
    Model representing a Point of Contact (POC) profile for a partner's agency.

    Attributes:
        user: A ForeignKey to a user model, which is nullable and associated with the 'partner_user' related name.
        Name: The full name of the partner's POC.
        Address: The address of the partner's POC.
        Zip_Code: The postal code related to the partner's POC address.
        City: The city where the partner's POC is located.
        Country: A ForeignKey to a country model, representing the country of the POC's location.
        email: The business email of the partner's POC.
        email_verified: A Boolean indicating if the POC's business email has been verified.
        Telephone: The business telephone number of the partner's POC.
        HashKey: A unique identifier hash key for the partner's POC.
        Registration: The date and time of registration for the partner's POC.
        Extra_record: A Text field containing extra JSON formatted records related to the POC.
        Observation: Text field for additional observations about the partner's POC.
        Category: A ForeignKey to the jobpoc model, which specifies the category of the POC.
        Language1: A ForeignKey to the Language model representing the POC's primary language.
        Language2: A ForeignKey to the Language model representing the POC's secondary language if any.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True, blank=True, related_name='POC_Agency')    
    
    Name = models.CharField(max_length=100, blank=True, help_text = "ARepresentativegency Name") # Representative name
    Address = models.CharField(max_length=100, blank=True, help_text = "Address") # Representative address
    Zip_Code = models.CharField(max_length=100, blank=True, help_text = "Zip Code.") # Zip Code
    Country = models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Country", related_name='POC_Country') 
    email = models.CharField(max_length=50, blank=True, help_text = "Business email.")
    email_verified  = models.BooleanField(default=False, help_text = "True if email was verified") 
    Telephone = models.CharField(max_length=15, blank=True, help_text = "Business telephone.") # The contact number  
    HashKey = models.CharField(max_length=40, editable=True, blank=True, help_text = "Hash key to identity Representative")
    Registration = models.DateTimeField(default=timezone.now)  
    Extra_record  = models.TextField(max_length=1000, blank=True, help_text = "JSON: extra records.")
    Observation  = models.TextField(max_length=1000, blank=True, help_text = "Observation about Representative.")
    Category = models.ForeignKey(jobpoc,on_delete=models.SET_NULL,  null=True, blank=True, related_name='POC_category')    
    Language1 = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, help_text = "POC_Language 1", related_name='POC_Language1') 
    Language2 = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, help_text = "POC Language 2", related_name='POC_Language2') 
    
    class Meta:
            verbose_name_plural = "Partner POCs"
        
    def __str__(self):
        """
        String for representing the Model object in the admin interface and anywhere else the model is referenced.
        """
        return self.Name

    def save(self,force_insert=False, force_update=False, using=None):
        """
        Overwrites the save method to perform custom actions such as generating a unique HashKey for new POC records.
        """
        if not self.HashKey:
            data = datetime.date.today()
            time = datetime.datetime.today()
            code = str(self.pk)+str(data)+str(time)
            self.HashKey = hashlib.sha1(code.encode()).hexdigest()[:30] 
            
        try:
            return super(partnerpoc, self).save()
        except IntegrityError:
            return HttpResponse("ERROR: this POC can not be saved...") 

class coverage(models.Model):
    """
    Model representing the geographic coverage area and service type for a partner's offerings.

    Attributes:
        user: A ForeignKey reference to the user model, indicating the user associated with the coverage.
        Country: The name of the country where the service coverage applies.
        DistrictRegion: The name of the district or region where the service coverage applies.
        CityMunicipality: The name of the city or municipality where the service coverage applies.
        ServiceCategory: A ForeignKey to the ServiceCategory model, specifying the type of services covered.
    """
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name='coverage_user')    
    
    Country = models.CharField(max_length=30, blank=True, help_text = "Country") 
    DistrictRegion = models.CharField(max_length=30, blank=True, help_text = "District/Region") 
    CityMunicipality = models.CharField(max_length=30, blank=True, help_text = "City/Municipality") 
    ServiceCategory = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Service type") 
    
    class Meta:
            verbose_name_plural = "APP Coverage"

