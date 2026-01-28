"""
Kit Administration - Suroga API

This module configures the administrative interface for managing kits within the Suroga API. It utilizes Django's
admin module to create an admin interface for the Kit app models. Admin classes are defined here to customize
the appearance and functionality of the Kit model views within the Django admin site.

Included Admin Classes:
    - KitTypeAdmin: Manages the display and organization of KitType entities.
    - KitStockAdmin: Provides administration options for KitStock inventory records.
    - OperationTypeAdmin: Facilitates the categorization of various operation types.
    - OperationLogAdmin: Tracks and reviews operation logs related to kits.

By registering the app's models along with their respective Admin classes, the admin interface is enhanced
to provide customized displays for managing kit-related data efficiently and intuitively.

Usage:
    - The Django admin site uses these configurations to provide a user interface for administrative staff.
    - Admin classes determine how records are listed, edited, and displayed in the backend dashboard.

Please ensure proper registration of model Admin classes and consistent updates to the configurations
to match the evolving requirements of the administrative operations.

Maintainer: Carlos Leandro
Last Modified: 15/3/2024

Example:
    The registrations of admin classes use the Django admin.site.register() function to link each model
    to its specific Admin class.
"""
from django.contrib import admin

# Register your models here.

from kit.models import kittype, kitstock, operationtype, operationlog

class kittypeAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for KitType model.

    Displays the `pk` and `KitTypeName` in the admin list view to easily identify different kit types.
    """
    list_display = (
    'pk',
    'KitTypeName',
    )
# Registers KitType model for admin management using the kittypeAdmin configuration
admin.site.register(kittype,kittypeAdmin)

class kitstockAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for KitStock model.

    Defines a detailed view of kit stock items, including their type, reference number, and location content.
    """
    list_display = (
    'pk',
    'KitType',
    'Kit_Ref_Numer',
    'Location',
    'Content'
    )
# Registers KitStock model for admin management using the kitstockAdmin configuration
admin.site.register(kitstock,kitstockAdmin)

class operationtypeAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for OperationType model.

    Provides a concise view featuring the `pk` and `OperationTypeName`, helping to distinguish operation types.
    """
    list_display = (
    'pk',
    'operationTypeName',
    )

# Registers OperationType model for admin management using the operationtypeAdmin configuration
admin.site.register(operationtype,operationtypeAdmin)

class operationlogAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for OperationLog model.

    Allows administrators to view logs of operations performed, their types, and
    statuses related to expected arrival, delivery, and reception.
    """
    list_display = (
    'pk',
    'Kit',
    'Description',
    'DateTime',
    'OperationType',
    'ContractSectionA',
    'ExpectedArrivalDate',
    'ConfirmationFromSectionA',
    'ContractSectionD',
    'DeliveryFromSectionD',
    'ReceptionFromSectionD',
    )
# Registers OperationLog model for admin management using the operationlogAdmin configuration
admin.site.register(operationlog,operationlogAdmin)
