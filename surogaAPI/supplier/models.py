"""
Suroga Supplier App - Models Configuration

This module defines the data models for the Supplier application within the Suroga API project. By leveraging
Django's Object-Relational Mapping (ORM), these models represent the various entities and their interactions
as part of the app's domain. This includes profiles for agencies and representatives, contract details,
service types, communication channels, and many more.

Each class within this module corresponds to a table in the database, with fields representing the table
columns and relationships among tables mirroring the associations between the entities these models depict.
Furthermore, custom methods are added to some models to encapsulate logic related to the creation, update,
and retrieval of instances.

Highlights:
    - ForeignKey relationships to embody many-to-one associations.
    - Fields with various data types to accurately represent different properties of an entity.
    - Custom save methods to apply business rules and data integrity checks during the persistence of a model.
    - Meta subclass within each model to provide metadata and custom behavior.
    - Rich text-based help fields to guide the user/administrator through the Django admin interface.

References:
    - Django model field reference: https://docs.djangoproject.com/en/4.0/ref/models/fields/
    - Django model instance methods: https://docs.djangoproject.com/en/4.0/ref/models/instances/

Caution: Direct modifications to this file can affect the database schema and application behavior. Ensuring
that any changes follow Django's best practices and are coupled with appropriate migrations is critical to the
stability and integrity of the application's data.

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

from core.models import equipment,country, districtregion, citymunicipality, RideDuration, image, sound, localwifi, publicevent


#from supplier.models import requisitiontype, selectiontype, offertype, informationtype, identificationtype, protocol, profileagency, reprecategory, profilerepresentative, contracttype, contractpaymenttype, contractpricetype, contract, contractsection, contractsectionchannels, servicetype, commtype, commlog

# Create your models here.
class requisitiontype(models.Model):
    """
    Represents types of requisitions available for requesting a surrogate service.
    
    Attributes:
        requisition: Human-readable text indicating the type of requisition method available.
    """
    requistion = models.CharField(max_length=50, unique=True, blank=False, help_text = "Requisition type")
     
    class Meta:
        verbose_name_plural = "Requisition type"
    def __str__(self):
        return self.requistion

class selectiontype(models.Model):
    """
    Denotes how surrogates are offered for selection by the service.
    
    Attributes:
        selection: A choice between single or multiple surrogate selection methods.
    """
    selection = models.CharField(max_length=50, unique=True, blank=False, help_text = "selection type")
     
    class Meta:
        verbose_name_plural = "Selection Types"
    def __str__(self):
        return self.selection


class offertype(models.Model):
    """
    Categorizes types of offers provided by the service.
    
    Attributes:
        offer: Details about the service offer like single or multiple options.
    """
    offer = models.CharField(max_length=50, unique=True, blank=False, help_text = "Offer type")
     
    class Meta:
        verbose_name_plural = "Offer Types"
    def __str__(self):
        return self.offer

class informationtype(models.Model):
    """
    Captures the kinds of information available about surrogates.
    
    Attributes:
        information: Description of the data provided about the surrogate.
    """
    information = models.CharField(max_length=50, unique=True, blank=False, help_text = "Information type")
     
    class Meta:
        verbose_name_plural = "Information Types"
    def __str__(self):
        return self.information

class identificationtype(models.Model):
    """
    Lists identifiable types for surrogates.
    
    Attributes:
        identification: Describes the means of identifying surrogates.
    """
    identification = models.CharField(max_length=50, unique=True, blank=False, help_text = "Identification type")
     
    class Meta:
        verbose_name_plural = "Identification Types"
    def __str__(self):
        return self.identification

class protocol(models.Model):
    """
    Details the agency's protocol for offering surrogate services.
    
    Attributes:
        Agency: Reference to the User model for the agency.
        Is_API: Flags if the agency employs an API.
        API_tested: Confirms if the agency's API is tested.
        API_ID: The API key or identifier if an API is used.
        WebSite: Official website or API endpoint URL.
        type_requisition: Links to the type of requisition used.
        type_selection: Links to the surrogate selection type.
        type_offer: Connects to the offer type used by the agency.
        type_information: Associates with the information type about surrogates.
        type_identification: Relates to the identification type used.
        Registration: Timestamp when the entry was made or updated.
    """
    Agency = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Agency", related_name='protocol_agency') 
    Is_API = models.BooleanField(default=False, help_text = "Agency has an API")  
    API_tested = models.BooleanField(default=False, help_text = "API was tested")  
    API_ID = models.CharField(max_length=50, unique=True, blank=True, help_text = "API key")
    WebSite = models.CharField(max_length=50, unique=True, blank=True, help_text = "API root page")
    type_requisition = models.ForeignKey(requisitiontype, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Requisition type", related_name='protocol_requisition') 
    type_selection = models.ForeignKey(selectiontype, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Selection type", related_name='protocol_selectionr') 
    type_offer = models.ForeignKey(offertype, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Offer type", related_name='protocol_offer') 
    type_information = models.ForeignKey(informationtype, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Information type", related_name='protocol_information') 
    type_identification = models.ForeignKey(identificationtype, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Identification type", related_name='protocol_identification') 
    Registration = models.DateTimeField(default=timezone.now, help_text="Time of protocol creation or update")  
     
    class Meta:
        verbose_name_plural = "Protocol"
    def __str__(self):
        # Return the agency's username with a check if the Agency exists to prevent errors.
        return self.Agency.username if self.Agency else 'Unknown'


class profileagency(models.Model):

    """
    Model representing an agency's profile within the supplier app.
    
    Attributes:
        user: A foreign key to the Django's built-in User model, set to NULL if the related user is deleted.
        Name: The name of the agency (optional field).
        Address: The physical address of the agency (optional field).
        Zip_Code: The postal code for the agency's location (optional field).
        Country: A foreign key to another model 'country' representing the agency's country (optional field).
        Telephone: Contact telephone number for the agency (optional field).
        ITIN: Agency's Individual Tax Identification Number (optional field).
        IBAN: The International Bank Account Number associated with the agency (optional field).
        HashKey: A unique hash key to identify the agency, generated if not provided (not editable).
        Registration: The date and time when the agency profile was registered (non-editable, set to the current time by default).
        Website: The URL to the agency's official website (optional field).
        Stripe_ID: An identifier used for processing payments through Stripe (optional field).
        Extra_record: A text field to store extra records in a JSON format (optional field).
        Observation: A text field for any additional observations about the agency (optional field).
    """
    
    # Fields with types, constraints and help texts
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=False, related_name='agency_user')    
    
    Name = models.CharField(max_length=100, blank=True, help_text = "Agency Name") # Agency name
    Address = models.CharField(max_length=100, blank=True, help_text = "Address") # Agency address
    Zip_Code = models.CharField(max_length=100, blank=True, help_text = "Zip Code.") # Zip Code
    Country = models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Country", related_name='agency_Country') 
    Telephone = models.CharField(max_length=100, blank=True, help_text = "Business telephone.") # The contact number  
    ITIN = models.CharField(max_length=40, editable=True, blank=True, help_text = "Individual Tax Identification Number")    
    IBAN = models.CharField(max_length=40, editable=True, blank=True, help_text = "Agency IBAN")    
    HashKey = models.CharField(max_length=40, editable=False, blank=True, help_text = "Hash key to identity Agency")
    Registration = models.DateTimeField(default=timezone.now, editable=False)  
    Website = models.URLField(default='',blank=True, help_text = "Agency Website. ")  
    Stripe_ID = models.CharField(max_length=10, editable=True, blank=True, default='', help_text = "Agency ID")
    Extra_record  = models.TextField(max_length=1000, blank=True, help_text = "JSON: extra records.")
    Observation  = models.TextField(max_length=1000, blank=True, help_text = "Observation about Agency.")
    
    class Meta:
        verbose_name_plural = "Agency profile"
        
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.Name

    def save(self,force_insert=False, force_update=False, using=None):

        """
        Overwrites the save method to generate a hash key for the agency profile if not already set.
        """
        if not self.HashKey:
            # Generating the HashKey from the primary key, current date and time
            data = datetime.date.today()
            time = datetime.datetime.today()
            code = str(self.pk)+str(data)+str(time)
            self.HashKey = hashlib.sha1(code.encode()).hexdigest()[:30] 
            
        try:
            # Attempt to save the instance using superclass's save method
            return super(profileagency, self).save()
        except IntegrityError:
            # Handling the IntegrityError in the unlikely event it is raised
            return HttpResponse("ERROR: this agency can not be saved...") 

class reprecategory(models.Model):
    """
    Model for listing categories of representatives within the supplier app.

    Attributes:
    - JobCategory: The category title of a representative; a required field and must be unique.
    """

    JobCategory = models.CharField(max_length=50, unique=True, blank=False, help_text = "Representative category")
     
    class Meta:
        # Plural name for admin panel
        verbose_name_plural = "Representative category"
    def __str__(self):
        # Representation of the model object in human-readable form
        return self.JobCategory

class profilerepresentative(models.Model):

    """
    Model representing an individual representative's profile.

    Attributes:
    - user: A ForeignKey to Django's built-in User model, set to NULL if the related user is deleted.
    - Name: The representative's name; an optional field.
    - Address: The representative's address; an optional field.
    - Zip_Code: The zip code for the representative's address; an optional field.
    - Country: A ForeignKey to the 'country' model; an optional field.
    - Telephone: The representative's business telephone number; an optional field.
    - HashKey: An automatically generated unique hash key to identify the representative; not editable.
    - Registration: The date and time of registration; non-editable, automatic timestamp.
    - Agency: A ForeignKey linking to a 'profileagency' representing the representative's agency; an optional field.
    - Extra_record: A TextField containing extra records in JSON format; an optional field.
    - Observation: A TextField for any additional notes about the representative; an optional field.
    - Category: A ForeignKey linking to the 'reprecategory' model; an optional field.
    """

    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=False, related_name='representative_user')    
    
    Name = models.CharField(max_length=100, blank=True, help_text = "ARepresentativegency Name") # Representative name
    Address = models.CharField(max_length=100, blank=True, help_text = "Address") # Representative address
    Zip_Code = models.CharField(max_length=100, blank=True, help_text = "Zip Code.") # Zip Code
    Country = models.ForeignKey(country, on_delete=models.SET_NULL, null=True, blank=True, help_text = "Country", related_name='representative_country') 
    Telephone = models.CharField(max_length=15, blank=True, help_text = "Business telephone.") # The contact number  
    HashKey = models.CharField(max_length=40, editable=False, blank=True, help_text = "Hash key to identity Representative")
    Registration = models.DateTimeField(default=timezone.now, editable=False)  
    Agency = models.ForeignKey(profileagency, on_delete=models.SET_NULL, null=True, blank=True,related_name='Agency')    
    Extra_record  = models.TextField(max_length=1000, blank=True, help_text = "JSON: extra records.")
    Observation  = models.TextField(max_length=1000, blank=True, help_text = "Observation about Representative.")
    Category = models.ForeignKey(reprecategory,on_delete=models.SET_NULL, null=True, blank=True,related_name='representative_category')    
    
    class Meta:
        # Plural name for admin panel
        verbose_name_plural = "Representative profile"
        
    def __str__(self):
        # Representation of the model object in human-readable form
        return self.Name

    # Custom save method to handle HashKey generation and catching IntegrityError can be written here.
    def save(self,force_insert=False, force_update=False, using=None):

        if not self.HashKey:
            data = datetime.date.today()
            time = datetime.datetime.today()
            code = str(self.pk)+str(data)+str(time)
            self.HashKey = hashlib.sha1(code.encode()).hexdigest()[:30] 
            
        try:
            return super(profilerepresentative, self).save()
        except IntegrityError:
            return HttpResponse("ERROR: this representative can not be saved...") 

class contracttype(models.Model):
    """
    Model for listing types of contracts.

    Attributes:
    - ContractTypeName: A unique name for a type of contract; a required field.
    """
    ContratctTypeName = models.CharField(max_length=50, unique=True, blank=False, help_text = "Contract Type")
     
    class Meta:
        # Plural name for admin panel
        verbose_name_plural = "Contract Types"
    def __str__(self):
        # Representation of the model object in human-readable form
        return self.ContratctTypeName


class contractpaymenttype(models.Model):
    """
    Model for listing types of contract payments.

    Attributes:
    - PaymentTypeName: A unique name for a payment type; a required field.
    """
    PaymentTypeName = models.CharField(max_length=50, unique=True, blank=False, help_text = "Payment Type")
     
    class Meta:
        # Plural name for admin panel
        verbose_name_plural = "Contract Payment Types"
    def __str__(self):
        # Representation of the model object in human-readable form
        return self.PaymentTypeName

class contractpricetype(models.Model):
    """
    Model for listing different types of pricing strategies or structures that can be applied to contracts.

    Attributes:
    - PriceTypeName: A name given to the specific price type; must be unique and is a required field.
    """
    # Field for storing the name of the price type
    PriceTypeName = models.CharField(max_length=50, unique=True, blank=False, help_text = "Price Type")
     
    class Meta:
        # Plural name for the admin panel to describe this collection of models
        verbose_name_plural = "Contract Price Types"
    def __str__(self):
        # Representation of the model object in human-readable form
        return self.PriceTypeName

class contract(models.Model):
    """
    Model for managing contracts between suppliers and other entities.

    Attributes:
    - Supplier: A ForeignKey to the User model representing the supplier involved in the contract. It can be null.
    - contract_type: A ForeignKey to the contracttype model that specifies the type of the contract. It can be null.
    - Contract_Date_start: The start date of the contract.
    - Contract_Date_expiration: The expiration or end date of the contract.
    - Contract_POC: A ForeignKey to the profilerepresentative model; the Point of Contact (POC) for the contract. It can be null.
    - Payment_type: A ForeignKey to the contractpaymenttype model describing how payments are to be made. It can be null.
    - Price_type: A ForeignKey to the contractpricetype model specifying the pricing structure. It can be null.
    - Registration: The date and time the contract was registered; not editable.
    - is_active: A Boolean indicating whether the contract is currently active.
    """
    # Relationships to other models and essential fields
    Supplier = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True, related_name='contract_supplier')    
    contract_type = models.ForeignKey(contracttype,default='', on_delete=models.SET_NULL, null=True, blank=True, related_name='contract_type')
    Contract_Date_start = models.DateField(default=timezone.now, help_text = "contract Start")
    Contract_Date_expiration = models.DateField(default=timezone.now, help_text = "contract Deadline")
    Contract_POC = models.ForeignKey(profilerepresentative,on_delete=models.SET_NULL, null=True, blank=True,related_name='contract_POC')    
    Payment_type = models.ForeignKey(contractpaymenttype,on_delete=models.SET_NULL,null=True, blank=True, related_name='contract_payment')    
    Price_type = models.ForeignKey(contractpricetype,on_delete=models.SET_NULL,null=True, blank=True, related_name='contract_price')    
    Registration = models.DateTimeField(default=timezone.now, editable=False)  
    is_active = models.BooleanField(default=True, help_text = "True if contract is active")  
    class Meta:
        verbose_name_plural = "Contracts"

class contractsection(models.Model):
    """
    Model for managing specific sections or clauses within a contract.

    Attributes:
    - contract: A ForeignKey to the contract model that this section belongs to. It can be null.
    - Country: A ForeignKey to the country model specifying the country of operation or relevance for the section. It can be null.
    - DistrictRegion: A ForeignKey to the districtregion model; the region or district mentioned in the section. It can be null.
    - CityMunicipality: A ForeignKey to the citymunicipality model; the city or municipality covered by the section. It can be null.
    - RequiredMaxConfigTime: A DecimalField specifying the maximum allowable time for configuration or setup in hours.
    - SectonStock: A TextField containing a JSON description of the stock associated with the section, if any.
    - Registration: The date and time the section was registered; not editable.
    - is_active: A Boolean indicating whether the contract section is currently active.
    - variante: A TextField containing a JSON description of any variants or special conditions of the contract section.
    """
    # Relationships to other models and additional fields for storing contract details
    contract = models.ForeignKey(contract,on_delete=models.SET_NULL, null=True, blank=True,help_text = "contract", related_name='section_contract')
    Country = models.ForeignKey(country,on_delete=models.SET_NULL,null=True, blank=True, help_text = "Country", related_name='section_country')
    DistrictRegion = models.ForeignKey(districtregion,on_delete=models.SET_NULL, null=True, blank=True,help_text = "District/Region", related_name='section_district')
    CityMunicipality = models.ForeignKey(citymunicipality,on_delete=models.SET_NULL,null=True, blank=True, help_text = "City/Municipality", related_name='section_municipality')
    RequiredMaxConfigTime = models.DecimalField(max_digits=5, decimal_places=1, default=0, help_text = "Required Max Config Time (hours)")  
    SectonStock = models.TextField(max_length=1000, blank=True, help_text = "JSON: Section stock description")
    Registration = models.DateTimeField(default=timezone.now, editable=False)  
    is_active = models.BooleanField(default=True, help_text = "True if contract is active") 
    variante = models.TextField(max_length=1000, blank=True, help_text = "JSON: contract variant") 

    class Meta:
        verbose_name_plural = "Contract Sections"


class contractsectionchannels(models.Model):
    """
    Model for representing communication channels associated with a particular contract section.

    Attributes:
    - ContractSection: A ForeignKey to the contractsection model that this communication channel is related to.
    - CommOrderSaToSupp: A ForeignKey to a profilerepresentative model for communication from sales assistant to supplier.
    - CommRideSuppToSa: A ForeignKey to a profilerepresentative model for communication from supplier to sales assistant regarding rides.
    - CommOrderSaToSupp: A ForeignKey to a profilerepresentative model for communication regarding orders from sales assistant to supplier. (Duplicate field, likely a mistake.)
    - CommOrderSuppToSa: A ForeignKey to a profilerepresentative model for communication regarding orders from supplier to sales assistant.
    - CommInvoice: A ForeignKey to a profilerepresentative model for communication regarding invoices.
    - CommPaymConfirm: A ForeignKey to a profilerepresentative model for confirming payments.
    """
    # Relationships to other models. Please note there seems to be an error with duplicate field 'CommOrderSaToSupp', which should be addressed.
    ContractSection = models.ForeignKey(contractsection,on_delete=models.SET_NULL, null=True, blank=False, related_name='channel_section')    
    CommOrderSaToSupp = models.ForeignKey(profilerepresentative,on_delete=models.SET_NULL, null=True, blank=True,related_name='channel_comm1')    
    CommRideSuppToSa = models.ForeignKey(profilerepresentative,on_delete=models.SET_NULL, null=True, blank=True,related_name='channel_comm2')    
    CommOrderSaToSupp = models.ForeignKey(profilerepresentative,on_delete=models.SET_NULL, null=True, blank=True,related_name='channel_comm3')    
    CommOrderSuppToSa = models.ForeignKey(profilerepresentative,on_delete=models.SET_NULL, null=True, blank=True,related_name='channel_comm4')    
    CommInvoice = models.ForeignKey(profilerepresentative,on_delete=models.SET_NULL, null=True, blank=True,related_name='channel_comm5')    
    CommPaymConfirm = models.ForeignKey(profilerepresentative,on_delete=models.SET_NULL, null=True, blank=True,related_name='channel_comm6')    

    class Meta:
        verbose_name_plural = "Contract Section Channels"

class servicetype(models.Model):
    """
    Model for categorizing different types of provided services.

    Attributes:
    - Name: The unique name of the service.
    - Duration: A ForeignKey to the RideDuration model relating to the duration of the service.
    - Equipment: A ForeignKey to the equipment model representing equipment associated with the service.
    - Image: A ForeignKey to the image model representing images associated with the service.
    - Sound: A ForeignKey to the sound model representing sound aspects of the service.
    - LocalWifi: A ForeignKey to the localwifi model representing wifi services involved.
    - PublicEvent: A ForeignKey to the publicevent model representing if the service involves public events.
    - ContractA to ContractF: Boolean fields to indicate if the service requires different types of contracts.
    - ServiceRules: A TextField to store service rules in a JSON format.
    - ServiceSetting: A TextField to store service settings in a JSON format.
    """
    Name = models.CharField(max_length=50, unique=True, blank=False, help_text = "Service name")
    Duration = models.ForeignKey(RideDuration,on_delete=models.SET_NULL, null=True, blank=True,related_name='service_Duration') 
    Equipment = models.ForeignKey(equipment,on_delete=models.SET_NULL, null=True, blank=True,related_name='service_Image')
    Image = models.ForeignKey(image,on_delete=models.SET_NULL, null=True, blank=True,related_name='service_Image')
    Sound = models.ForeignKey(sound,on_delete=models.SET_NULL, null=True, blank=True,related_name='service_Sound')
    LocalWifi = models.ForeignKey(localwifi,on_delete=models.SET_NULL, null=True, blank=True,related_name='service_Wifi')
    PublicEvent = models.ForeignKey(publicevent,on_delete=models.SET_NULL, null=True, blank=True,related_name='service_Event')
    ContractA = models.BooleanField(default=False, help_text = "True if requires type A contract") 
    ContractB = models.BooleanField(default=False, help_text = "True if requires type B contract") 
    ContractC = models.BooleanField(default=False, help_text = "True if requires type C contract") 
    ContractD = models.BooleanField(default=False, help_text = "True if requires type D contract") 
    ContractE = models.BooleanField(default=False, help_text = "True if requires type E contract") 
    ContractF = models.BooleanField(default=False, help_text = "True if requires type F contract") 
    ServiceRules = models.TextField(max_length=1000, blank=True, help_text = "JSON: Service rules") 
    ServiceSetting = models.TextField(max_length=1000, blank=True, help_text = "JSON: Service rules")
    class Meta:
        verbose_name_plural = "Service Types"
    def __str__(self):
        return self.Name


class commtype(models.Model):
    """
    Model for listing communication types, such as email, phone call, messaging app, etc.

    Attributes:
    - CommTypeName: The unique name of the communication type; a required field.
    """
    CommTypeName = models.CharField(max_length=50, unique=True, blank=False, help_text = "Communication Type")
     
    class Meta:
        verbose_name_plural = "Communication Types"
    def __str__(self):
        return self.CommTypeName



