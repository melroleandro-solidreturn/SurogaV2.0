"""
Partner Administration - Suroga API

This module configures the admin interface for the Partner app within the Suroga API project.
It leverages Django's admin.ModelAdmin class to customize the admin panel for the partner models,
allowing administrators to easily add, modify, and delete partner data.

Administrative interface classes such as 'coverageAdmin', 'profilepartnerAdmin', 'jobpocAdmin',
and 'partnerpocAdmin' are defined here to fine-tune the presentation and capabilities of the
admin list view as per the requirements of Suroga API's data management.

By registering models with their respective admin classes, these configurations become effective 
in the admin site, providing a user-friendly and efficient way to manage partner-related information.

Recommended Usage:
    - Refine or expand the list_display attributes to include fields most critical for the admin users.
    - Leverage Django's admin functionalities like 'list_filter', 'search_fields', and 'ordering' to improve data browsing capabilities.

Important:
    - Changes to the admin interface should always be preceded by careful consideration and thorough testing in a development environment to ensure they meet the requirements and do not negatively impact the user experience.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""
from django.contrib import admin

# Register your models here.
from partner.models import coverage, profilepartner, jobpoc, partnerpoc

class coverageAdmin(admin.ModelAdmin):
    """
    Configures the Django admin interface for the 'coverage' model.

    This admin class defines the display of the geographical coverage within the admin list view.
    """
    list_display = (
    'pk',
    'Country',
    'DistrictRegion',
    'CityMunicipality',
    'ServiceCategory',
    )
# Registers the 'coverage' model for management in the admin interface
admin.site.register(coverage,coverageAdmin)

class profilepartnerAdmin(admin.ModelAdmin):
    """
    Customizes the Partner Profile model view in the Django admin interface.

    Allows administrators to oversee partner profiles, including verification statuses and API activation.
    """
    list_display = (
    'pk',
    'Validated_profile',
    'user',
    'Name',
    'Country',
    'Language',
    'Telephone',
    'API_activated',
    'Address_verified',
    'Telephone_verified',
    'ITIN_verified',
    'IBAN_verified',
    'Google_play_verified',
    'Apple_store_verified',
    'webwooks_suroo_verified',
    )
# Registers the 'profilepartner' model for management in the admin interface
admin.site.register(profilepartner,profilepartnerAdmin)

class jobpocAdmin(admin.ModelAdmin):
    """
    Admin interface settings for the Job Point of Contact (POC) model.

    Offers a simplified list view showcasing POC categories.
    """
    list_display = (
    'pk',
    'JobCategory',  # Displays the job category of the partner's POC
    )
# Registers the 'jobpoc' model for management in the admin interface
admin.site.register(jobpoc,jobpocAdmin)


class partnerpocAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Points of Contact (POC) associated with partner profiles.

    The list view provides quick access to key details such as the partner's name, email, and telephone.
    """
    list_display = (
    'pk',
    'user', # User entity associated with the POC
    'Category', # POC's job category
    'Name',
    'email',
    'Telephone',
    )
admin.site.register(partnerpoc,partnerpocAdmin)

