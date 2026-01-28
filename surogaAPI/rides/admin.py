"""
Rides App Administration - Suroga API

This module defines custom Django admin classes for the 'rides' app within the Suroga API project.
It configures the admin interface for various models such as Contract Section Ride Market, 
Meeting Log, Communication Log, and Message Board, making each of these models editable through
Django's built-in admin interface. Each admin class specifies the fields to be displayed in the list view,
providing the administrators with a convenient way to oversee and manage application-related data.

The admin classes utilize the Django ModelAdmin to customize the admin panel's display, forms, and other behaviors.

Usage:
    - Register model classes with their corresponding ModelAdmin subclasses to customize admin interfaces.
    - Use list_display to control which model fields are displayed in the admin's list views for each model.

Notes:
    - Make sure all models that require admin interface representation are properly registered.
    - Changes to admin configurations should be rigorous as they impact the admin panel's functionality and UX.

Recommended reading:
    - Django admin site documentation: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
    - Django ModelAdmin documentation: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#modeladmin-objects

Maintainer: Carlos Leandro
Last Modified: 15/3/2024
"""

from django.contrib import admin

# Register your models here.
from rides.models import rating, ServiceCategory, ridetype, Ride, Booking
from rides.models import bookinglog, MessageBoard, paymentlog, ContrSectionRideMkt, mettinglog, commlog 

class bookinglogAdmin(admin.ModelAdmin):
    list_display = (
    'pk',
    'user',
    'OperationType',
    'Ride',
    'Booking',
    'RegistrationDate',
    )
# Registers the paymentlog model with the paymentlogAdmin configuration for the admin site
admin.site.register(bookinglog,bookinglogAdmin)

class paymentlogAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the paymentlog model.

    The list_display attribute specifies which fields to display in the admin list view.
    """
    list_display = (
    'pk',
    'PlantformUserType',
    'user',
    'OperationType',
    'SettlementDate',
    'PaymMethodResul',
    'StripTransactionID',
    'Ride',
    'Booking',
    'Value',
    'is_debit',
    'RegistrationDate',
    )
# Registers the paymentlog model with the paymentlogAdmin configuration for the admin site
admin.site.register(paymentlog,paymentlogAdmin)


class ratingAdmin(admin.ModelAdmin):
    """
    Configures the admin list view for the rating model to include specific fields.

    Allows admin users to easily view and manage ratings in the admin interface.
    """
    list_display = (
    'pk',
    'Name',
    'value',
    )
# Register rating model to be managed in admin
admin.site.register(rating,ratingAdmin)

class ServiceCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ServiceCategory model in the admin list view.

    Facilitates management of service category entries for admin users.
    """
    list_display = (
    'pk',
    'Name',
    )
# Register ServiceCategory model to be managed in admin
admin.site.register(ServiceCategory,ServiceCategoryAdmin)

class ridetypeAdmin(admin.ModelAdmin):
    """
    Customizes the display of ridetype entities in the Django admin interface.

    Ease of viewing and editing ridetype entries in the admin panel.
    """
    list_display = (
    'pk',
    'Name',
    )
# Register ridetype model to be managed in admin
admin.site.register(ridetype,ridetypeAdmin)

class RideAdmin(admin.ModelAdmin):
    """
    Admin interface settings for the Ride model for detailed list view representation.

    Fields provided offer a relevant snapshot of ride information for admin users.
    """
    list_display = (
    'pk',
    'user',
    'CityMunicipality',
    'DistrictRegion',
    'Country',
    'PayedAtRegistration',
    #'ServiceCategory',
    'ServiceTitle',
    #'ExpectDuration',
    'RegistrationDate',
    'Blocked',
    'Canceled',
    'Deleted',
    'Request_Id'
    )
# Register Ride model to be managed in admin
admin.site.register(Ride,RideAdmin)


class BookingAdmin(admin.ModelAdmin):
    """
    Defines admin settings for the Booking model, with customization on the list view.

    Enables admins to see the status and important details of bookings at a glance.
    """
    list_display = (
    'pk',
    'ride',
    'RegistrationDate',
    'RideDate',
    'ServiceTitle',
    'ExpectDuration',
    'Canceled',
    'StockSelected',
    'RequisitsSatisfied',
    'Expired',
    'Error',
    'Disputed',
    'ExtraPrice',
    'RideStarted',
    'RideStartDate',
    'RideEnded',
    'RideEndDate',
    'Request_Id',
    )
# Register Booking model to be managed in admin
admin.site.register(Booking,BookingAdmin)

class ContrSectionRideMktAdmin(admin.ModelAdmin):
    """
    Admin interface customization for Contract Section Ride Market model.

    Provides a list view that highlights key information about each market item.
    """
    list_display = (
    'pk',
    'Name',
    'Selected',
    'Ride',
    'ContractSectionA',
    'ContractSectionB',
    'ContractSectionC',
    'ContractSectionD',
    'ContractSectionE',
    'ContractSectionF',
    'KitType',
    'KitRequired',
    'TotalPrice',
    )
# Registration of the admin class for Contract Section Ride Market model
admin.site.register(ContrSectionRideMkt,ContrSectionRideMktAdmin)

class mettinglogAdmin(admin.ModelAdmin):
    """
    Custom admin display for meeting log entries.

    Aligns with the admin interface for clear inventory of meeting records related to rides.
    """
    list_display = (
    'pk',
    'Ride',
    'ActionType',
    'DateTime', # Displays when the action within a meeting took place.
    'Satus', # Denotes the status of the meeting.
    )
# Registration of the admin class for meeting log model
admin.site.register(mettinglog,mettinglogAdmin)

class commlogAdmin(admin.ModelAdmin):
    """
    Configures admin list display for communication logs.

    Offers a detailed view of communication events between users and contract sections.
    """
    list_display = (
    'pk', 
    'Comm_Type', # Indicates the type of communication that took place.
    'Ride',
    'Contract', # Show which contract section is associated with the communication.
    'DateTime', # Records the time of the communication.
    'Message',  # The actual content of the communication.
    )
# Registration of the admin class for communication log model
admin.site.register(commlog,commlogAdmin)

class MessageBoardAdmin(admin.ModelAdmin):
    """
    Defines settings for the MessageBoard model in the Django admin interface.

    Provides quick administrative insight into the read status, deletion, and abuse reports
    for messages related to booking operations.
    """
    list_display = (
    'pk',
    #'Date',
    #'user',
    #'booking',
    'Read',    # Indicates if the message was read.
    'deleted', # Shows if the message was deleted by the sender.
    'Abuse',   # Highlights if the message was reported as abusive by the recipient.
    )
# Registration of the admin class for Message Board model
admin.site.register(MessageBoard,MessageBoardAdmin)