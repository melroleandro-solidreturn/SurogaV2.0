"""
Kit Models - Suroga API

Defines the data models for the Kit application within the Suroga API.
These models represent the essential entities in the kit management system,
such as various types of kits, the stock of kits available, and the logs of
operations performed on them. The models are designed to capture all necessary
information to accurately track and manage kit-related data.

Models:
    - KitType: Describes the types of kits available.
    - KitStock: Manages the inventory of kits, including their types and quantities.
    - OperationType: Categorizes the types of operations that can be applied to kits.
    - OperationLog: Logs specific operations carried out on kit stocks.

Usage:
    These models should be referenced in views, forms, and other components
    that require interaction with kit-related data.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014

Remember to update the 'Last Modified' date whenever you make changes to this file.
"""
import datetime
import hashlib

from django.db import models, IntegrityError
from django.utils import timezone
from django.http import HttpResponse

from supplier.models import  contractsection


class kittype(models.Model):
    """
    Defines the type of kits available within the Partner app ecosystem.

    Attributes:
      KitTypeName: A human-readable name that uniquely identifies the type of kit.
    """
    KitTypeName = models.CharField(max_length=100, unique=True, blank=False, help_text = "Kit Type Name")

    class Meta:
        verbose_name_plural = "Kit Types"
    def __str__(self):
        """
        Returns a string representation of the Kit Type model, utilizing the KitTypeName.
        """
        return self.KitTypeName

class kitstock(models.Model):
    """
    Keeps an inventory of the kits including their types and content specifications.

    Attributes:
      KitType: Relates each stock item to a specific kit type.
      Kit_Ref_Number: A unique identifier for the kit stock item.
      Location: The stored location, potentially relating to a contract section.
      Content: A JSON field describing the contents of the kit.
    """
    KitType = models.ForeignKey(kittype, on_delete=models.SET_NULL, null=True, blank=False, help_text = "Kite type")  
    Kit_Ref_Numer = models.CharField(max_length=15, unique=True, blank=False, help_text = "Kit Ref number")
    Location = models.ForeignKey(contractsection , on_delete=models.SET_NULL, null=True, blank=True, help_text = "Location")  
    Content = models.TextField(max_length=1000, blank=True, help_text = "JSON: kit content") 

    class Meta:
        verbose_name_plural = "Kit Stock"
    def __str__(self):
        """
        Returns the unique reference number of the kit stock, aiding in its identification.
        """
        return self.Kit_Ref_Numer

class operationtype(models.Model):
    """
    Specifies the types of operations that can be performed on or with a kit in the system.

    Attributes:
      OperationTypeName: Name of the operation type, like 'maintenance' or 'replenishment'.
    """
    operationTypeName = models.CharField(max_length=50, unique=True, blank=False, help_text = "Operation Type")
     
    class Meta:
        verbose_name_plural = "Operation Types"

    def __str__(self):
        """
        Returns a string representation of the operation, utilizing the OperationTypeName.
        """
        return self.operationTypeName

class operationlog(models.Model):
    """
    Logs and tracks the details of operations performed on kits.

    Attributes:
      Kit: The kit on which the operation is performed.
      Description: Details of the operation.
      DateTime: Timestamp when the operation was logged.
      OperationType: The type of operation being logged.
      ContractSectionA: Links to a contract section involved in the operation.
      ExpectedArrivalDate: Predicted date of the kit's arrival for the operation.
      ConfirmationFromSectionA: Whether arrival has been confirmed by the contract party.
      ContractSectionD: Links to a contract section responsible for delivery.
      DeliveryFromSectionD: Whether delivery by Section D is confirmed.
      ReceptionFromSectionD: Whether reception from Section D is confirmed.
    """
    Kit = models.ForeignKey(kitstock,on_delete=models.SET_NULL, null=True, blank=False, help_text = "Kit", related_name='operation_kit')
    Description = models.CharField(max_length=100, unique=True, blank=False, help_text = "Operation description")
    DateTime = models.DateTimeField(default=timezone.now)  
    OperationType = models.ForeignKey(operationtype,on_delete=models.SET_NULL, null=True, blank=False, help_text = "Operation Type", related_name='operation_type')
    ContractSectionA = models.ForeignKey(operationtype,on_delete=models.SET_NULL, null=True, blank=False, help_text = "Contract A", related_name='operation_A')
    ExpectedArrivalDate = models.DateTimeField(default=timezone.now)   
    ConfirmationFromSectionA = models.BooleanField(default=False, help_text = "True if supplier confirmed kit arrivel.")
    ContractSectionD = models.ForeignKey(operationtype,on_delete=models.SET_NULL, null=True, blank=False, help_text = "Contract D", related_name='operation_De')
    DeliveryFromSectionD = models.BooleanField(default=False, help_text = "True if supplier confirmed kit delivery.")
    ReceptionFromSectionD = models.BooleanField(default=False, help_text = "True if supplier confirmed kit reception.")

    class Meta:
        verbose_name_plural = "Operation Log"

    def __str__(self):
        """
        Returns a string representation of the Operation Log based on the DateTime.
        """
        return str(self.DateTime)
