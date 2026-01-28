from django.contrib import admin

# Register your models here.
from core.models import time_zone, Language, Currency, country
from core.models import districtregion, citymunicipality, usertype, userprofile
from core.models import equipment, userloginlog, events, RideDuration
from core.models import version,  publicevent, sound, image, localwifi, commchannel

"""
Core Application Administration - Suroga API

This file configures the admin interface for the Core application of the Suroga API project. Each model within the
application has an associated admin class that defines how it should be displayed and manipulated within the Django
admin site. Customizations include defining the list of fields displayed in the admin list view, any fieldsets for
detail views, filters, search capabilities, and more.

The use of list_display is prevalent to ensure essential fields are immediately visible when admins list records
of each model. For models that are involved in user interaction logging, such as userloginlog, or manage static
reference data, such as time_zone or Language, the admin classes provide a clear, useful snapshot of each record
at a glance.

By registering these admin classes with the admin site, we enable site administrators to manage the data with ease,
utilizing the Django admin interface's powerful tools for querying and modifying data as needed.

Maintainer: Carlos Leandro
Last Modified: 15/3/2024

Refer to Django's admin documentation for additional details on admin site customization:
https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
"""

# Registers the `time_zone` model with Django's admin interface using a custom admin class.
# This allows for customization of how the time zones are displayed in the admin panel.
class time_zoneAdmin(admin.ModelAdmin):
    # Defines what information is displayed for each time zone entry in the list view of the admin.
    
	list_display = (
    'pk',
    'Name',
    'TimeZone',
    'UTCoffset',
    )
# Connects the model with the custom admin class so that it's used when displaying time zones in the admin.
admin.site.register(time_zone,time_zoneAdmin)

# Registration process is similar for the `Language` model.
# The LanguageAdmin class configures admin list view for `Language` objects.
class LanguageAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'Code',
    )
admin.site.register(Language,LanguageAdmin)


# CurrencyAdmin customizes the admin panel for `Currency` models,
# ensuring that currency names, their symbols, and positioning preferences are visible in the list view.
class CurrencyAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'Currency',
    'CurrencySymbol',
    'SymbolRight',
    )
admin.site.register(Currency,CurrencyAdmin)


# CountryAdmin enables the admin to manage `country` instances within the admin interface effectively,
# displaying a broad set of fields for comprehensive administrative visibility.
class CountryAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'Currency',
    'Language',
    'PhoneCode',
    'time_zone',
    'VAT',
    'GPS_latitude',
    'GPS_longitude',
    'ZoomLevel',
    'GoogleCode'
    )
admin.site.register(country,CountryAdmin)


# districtregionAdmin is similar to above admin classes,
# focusing on the district details, including GPS information and other identifiers.
class districtregionAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    #'Name',
    'GPS_latitude',
    'GPS_longitude',
    'ZoomLevel',
    'GoogleCode',
    )
admin.site.register(districtregion,districtregionAdmin)


# citymunicipalityAdmin is similar to above admin classes,
# focusing on the city and municipality details, including GPS information and other identifiers.
class citymunicipalityAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'districtregion',
    'GPS_latitude',
    'GPS_longitude',
    'ZoomLevel',
    'GoogleCode',
    )
admin.site.register(citymunicipality,citymunicipalityAdmin)

# usertypeAdmin configures the admin interface for User Type models, showing primary key and type name.
class usertypeAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'UserTypeName',
    )
admin.site.register(usertype,usertypeAdmin)


# userprofileAdmin presents relevant profile fields in the admin interface for UserProfile models.
class userprofileAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'user',
    'PlantformUserType',
    'email_confirmed',
    'Tele_confirmed',
    'is_blocked',
    'Language1',
    'Language1',
    'Paymentupdated',
    )
admin.site.register(userprofile,userprofileAdmin)


# userloginlogAdmin displays login log details in the admin panel, aiding in user activity tracking and debugging.
class userloginlogAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'user',
    'IP',
    'local',
    'region',
    'country',
    'lon',
    'lat',
    'geo_located',
    'RegistrationDate',
    )
admin.site.register(userloginlog,userloginlogAdmin)


# RideDurationAdmin organizes how Ride Duration models are represented in the admin list views.
class RideDurationAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Duration',
    'Token',
    )
admin.site.register(RideDuration,RideDurationAdmin)

# equipmentAdmin allows for management of equipment models, showcasing name and token.
class equipmentAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'Token',
    )
admin.site.register(equipment,equipmentAdmin)


# publiceventAdmin makes public event models manageable within the admin interface, presenting keys and names.
class publiceventAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'Token',
    )
admin.site.register(publicevent,publiceventAdmin)

# soundAdmin sets up the admin display for sound requirement models, providing quick reference with token information.
class soundAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'Token',
    )
admin.site.register(sound,soundAdmin)


# imageAdmin designed to streamline how image requirement models appear in admin with primary key and names.
class imageAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'Token',
    )
admin.site.register(image,imageAdmin)

# localwifiAdmin enables admin users to view and manage local Wi-Fi model data efficiently.
class localwifiAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Name',
    'Token',
    )
admin.site.register(localwifi,localwifiAdmin)

# eventsAdmin provides access to event models logging API requests, with request ID and type fields available.
class eventsAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'Request_Id',
    'Type',
    'Registration',
    )
admin.site.register(events,eventsAdmin)

# commchannelAdmin sets how communication channel models are navigated and managed within the admin interface, 
# especially for contact-related fields like emails.
class commchannelAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'mail_opr',
    'mail_api',
    'mail_ride',
    )
admin.site.register(commchannel,commchannelAdmin)

# versionAdmin organizes the admin representation for the versioning data of endpoint models, 
# displaying the endpoint name and related version numbers.
class versionAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'endpoint',
    'version',
    'RegistrationDate',
    )
admin.site.register(version,versionAdmin)