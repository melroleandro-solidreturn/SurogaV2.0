"""
Suroga Supplier App - Admin Configuration

This module defines the configuration for presenting Supplier app models
in the Django Administrator Site. It uses Django's in-built admin.ModelAdmin
subclassing to specify the layout and options for admin pages rendered for each
model.

With custom admin classes that extend admin.ModelAdmin, administrators can
customize how models are displayed, searched, and filtered, enhancing the
admin interface for entities such as contract sections, service types, and
communication types.

Each admin class defines a 'list_display' attribute determining which model fields
are displayed in the admin list view. The admin.site.register function binds these
classes to their respective models, activating them within the admin interface.

Usage:
    To include a model in the admin interface, define an admin class subclassing
    'admin.ModelAdmin', customize its presentation as necessary, and register it
    with the 'admin.site.register' call.

References:
    - Django admin site documentation: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
    - Django ModelAdmin documentation: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""
from django.contrib import admin

# Register your models here.
from supplier.models import requisitiontype, selectiontype, offertype, informationtype
from supplier.models import identificationtype, protocol, profileagency, reprecategory
from supplier.models import profilerepresentative, contracttype, contractpaymenttype
from supplier.models import contractpricetype, contract, contractsection
from supplier.models import contractsectionchannels, servicetype, commtype
from supplier.models import NUTSRegion

class requisitiontypeAdmin(admin.ModelAdmin):
	# Configuration for how 'requisitiontype' model should be displayed in the admin interface
    list_display = (
    'pk',
    'requistion',
    )
    # 'list_display' defines the fields of 'requisitiontype' model that appear in the list display

# Registers the 'requisitiontype' model with the admin interface using the 'requisitiontypeAdmin' class for settings
admin.site.register(requisitiontype,requisitiontypeAdmin)

class selectiontypeAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'selection',
    )
admin.site.register(selectiontype,selectiontypeAdmin)

class offertypeAdmin(admin.ModelAdmin):
	# Admin configuration for displaying 'selectiontype' model instances
    list_display = (
    'pk',
    'offer',
    )
# Registers the 'selectiontype' model with the admin interface
admin.site.register(offertype,offertypeAdmin)

class informationtypeAdmin(admin.ModelAdmin):
	# Defines how 'informationtype' model entries are represented in the admin list
    list_display = (
    'pk',
    'information',
    )
# Registration of the 'informationtype' model with the admin interface
admin.site.register(informationtype,informationtypeAdmin)


class identificationtypeAdmin(admin.ModelAdmin):
	# Sets up the admin list view for 'identificationtype' model
    list_display = (
    'pk',
    'identification',
    )
# Makes the 'identificationtype' model administrable through Django admin
admin.site.register(identificationtype,identificationtypeAdmin)

class protocolAdmin(admin.ModelAdmin):
	# Admin configuration that details how 'protocol' model instances are displayed
    list_display = (
    'pk',
    'Agency',
    'Is_API',
    'type_requisition',
    'type_selection',
    'type_offer',
    'type_information',
    'type_identification',
    )
# Registers the 'protocol' model with the admin interface
admin.site.register(protocol,protocolAdmin)

class profileagencyAdmin(admin.ModelAdmin):
	# Outlines the representation of 'profileagency' model instances in the admin interface
    list_display = (
    'pk',
    'user',
    'Name',
    'Address',
    'Zip_Code',
    'Country',
    'Telephone',
    )
# Adds the 'profileagency' model to the admin panel for managing those instances
admin.site.register(profileagency,profileagencyAdmin)

class reprecategoryAdmin(admin.ModelAdmin):
	# Specifies columns for 'reprecategory' model in Django admin list view
    list_display = (
    'pk',
    'JobCategory',
    )
# Registers the 'reprecategory' model and applies 'reprecategoryAdmin' class configurations to the admin interface
admin.site.register(reprecategory,reprecategoryAdmin)

class profilerepresentativeAdmin(admin.ModelAdmin):
	# Defines the representation of 'profilerepresentative' model instances with selected fields in the admin list view
    list_display = (
    'pk',
    'user',
    'Agency',
    'Category',
    'Name',
    'Telephone',
    )
# Registers 'profilerepresentative' for management via the admin interface with 'profilerepresentativeAdmin' settings
admin.site.register(profilerepresentative,profilerepresentativeAdmin)

class contracttypeAdmin(admin.ModelAdmin):
	# Sets the fields for 'contracttype' that will be shown in the admin interface list view
    list_display = (
    'pk',
    'ContratctTypeName',
    )
# Adds 'contracttype' model to Django admin and specifies the admin display settings with 'contracttypeAdmin' class
admin.site.register(contracttype,contracttypeAdmin)

class contractpaymenttypeAdmin(admin.ModelAdmin):
	# Configures how 'contractpaymenttype' is displayed in the admin panel, showing the primary key and payment type name
    list_display = (
    'pk',
    'PaymentTypeName',
    )
# Registers the 'contractpaymenttype' model with the admin site using the defined 'contractpaymenttypeAdmin' class
admin.site.register(contractpaymenttype,contractpaymenttypeAdmin)

class contractpricetypeAdmin(admin.ModelAdmin):
	# Customizes the admin list for 'contractpricetype' to display the ID and price type name
    list_display = (
    'pk',
    'PriceTypeName',
    )
# Registers 'contractpricetype' with the Django admin site and applies the 'contractpricetypeAdmin' configuration
admin.site.register(contractpricetype,contractpricetypeAdmin)

class contractAdmin(admin.ModelAdmin):
	# Admin configuration that enumerates the fields to show for 'contract' model list view in admin
    list_display = (
    'pk',
    'Supplier',
    'is_active',
    'contract_type',
    'Contract_Date_start',
    'Contract_POC',
    'Payment_type',
    'Price_type',
    )
# Allows the 'contract' model to be managed via the admin interface with the given 'contractAdmin' settings
admin.site.register(contract,contractAdmin)

class contractsectionAdmin(admin.ModelAdmin):
	# Decides which columns to display in the admin for 'contractsection', including status and related contract/detail fields
    list_display = (
    'pk',
    'is_active',
    'contract',
    #'CityMunicipality',
    #'DistrictRegion',
    #'Country',
    'RequiredMaxConfigTime',
    )
# Registers the 'contractsection' model to be administrable in the Django admin site with 'contractsectionAdmin' settings
admin.site.register(contractsection,contractsectionAdmin)

class contractsectionchannelsAdmin(admin.ModelAdmin):
	# Configures the admin panel list view for the 'contractsectionchannels' model.
    # list_display specifies the model fields to be displayed in the list view.
    list_display = (
    'pk', # The primary key of the record.
    'ContractSection', # ForeignKey pointing to a 'contractsection' instance.
    'CommOrderSaToSupp', # ForeignKey to a 'profilerepresentative' for one type of communication channel.
    'CommRideSuppToSa', # ForeignKey to a 'profilerepresentative' for another type of communication channel.
    'CommOrderSaToSupp',# Duplicate field name, likely an error; it should be unique or different from the previous one.
    'CommOrderSuppToSa',# ForeignKey to a 'profilerepresentative' for a different communication channel.
    'CommInvoice',# ForeignKey to a 'profilerepresentative' related to the invoice communication.
    'CommPaymConfirm',  # ForeignKey to a 'profilerepresentative' for payment confirmation communication.
    )
# Registers the 'contractsectionchannels' model for management with the defined admin class to the admin site.
admin.site.register(contractsectionchannels,contractsectionchannelsAdmin)

class servicetypeAdmin(admin.ModelAdmin):
	# This admin class outlines how instances of 'servicetype' will appear in the admin list view.
    # Fields listed in list_display are shown as columns on the list page.
    list_display = (
    'pk', # The primary key.
    'Name', # Name of the service type.
    'Duration',  # ForeignKey to another model defining the duration of the service.
    'Image',  # ForeignKey to a model that possibly holds images related to the service.
    'Sound', # ForeignKey to a model holding sound files related to the service.
    'LocalWifi', # ForeignKey to a model representing local wireless internet service.
    'PublicEvent',# ForeignKey to a model indicating if the service involves public events.
    'ContractB',# A series of boolean flags indicating if the service requires a specific type of contract.
    'ContractC',# A series of boolean flags indicating if the service requires a specific type of contract.
    'ContractD',# A series of boolean flags indicating if the service requires a specific type of contract.
    'ContractE',# A series of boolean flags indicating if the service requires a specific type of contract.
    'ContractF', # A series of boolean flags indicating if the service requires a specific type of contract.
    )
# Registers 'servicetype' model with the admin site and applies the 'servicetypeAdmin' class settings.
admin.site.register(servicetype,servicetypeAdmin)

class commtypeAdmin(admin.ModelAdmin):
	# Gestures how 'commtype' model instances will be administrated in the list view.
    list_display = (
    'pk', # The primary key of the record.
    'CommTypeName',  # The name of the communication type, a unique attribute of the model.
    
    )
# Activates the 'commtype' model in the Django admin and uses 'commtypeAdmin' class to define display settings.
admin.site.register(commtype,commtypeAdmin)

@admin.register(NUTSRegion)
class NUTSRegionAdmin(admin.ModelAdmin):
    # Campos que aparecerão na listagem
    list_display = ('postal_code', 'country_code', 'nuts0', 'nuts1', 'nuts2', 'nuts3')
    
    # Campos que terão links para edição
    list_display_links = ('postal_code',)
    
    # Campos que podem ser editados diretamente na listagem
    list_editable = ('country_code', 'nuts0')
    
    # Campos pelos quais podemos filtrar
    list_filter = ('country_code', 'nuts0', 'nuts1', 'nuts2')
    
    # Configuração avançada da busca
    search_fields = [
        'postal_code',
        'country_code',
        'nuts0',
        'nuts1',
        'nuts2',
        'nuts3',
    ]
    
    
    
    # Mostrar mais resultados por página
    list_per_page = 50
    
    # Preservar os filtros ao fazer buscas
    preserve_filters = True
    
    # Habilitar busca por relacionamentos
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            # Busca por código postal parcial
            queryset |= self.model.objects.filter(postal_code__icontains=search_term)
            
            # Busca hierárquica (ex: encontrar todos os códigos NUTS3 de um NUTS1)
            if search_term.upper().startswith('PT1'):
                queryset |= self.model.objects.filter(nuts1__iexact=search_term.upper())
        except:
            pass
        return queryset, use_distinct