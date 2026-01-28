"""
Partner App Forms - Suroga API

This module defines the forms used within the Partner application of the Suroga API. Forms in Django are
a flexible way of controlling user input on the frontend by providing fields for data entry and handling
form submissions on the backend.

The forms included here extend Django's default forms and form fields, customizing them for use cases specific
to the Partner application. Custom form fields and widgets, along with appropriate styling and validation, are
applied to ensure data integrity and user-friendly interfaces.

Usage:
    - Utilize these forms in views to handle GET and POST requests, process user data, and render form errors.
    - The forms are integrated with templates to present the correct context and collect user input.

Features:
    - Extends Django's built-in forms like 'UserCreationForm' and 'AuthenticationForm' for user authentication.
    - Model form integrations with 'partnerpoc', 'profilepartner', and other related models.
    - Client-side validation using custom widgets, classes, and placeholders.

References:
    - Django Forms documentation: https://docs.djangoproject.com/en/4.0/topics/forms/
    - Django Widgets reference: https://docs.djangoproject.com/en/4.0/ref/forms/widgets/

Changes should be thoroughly tested to prevent any data mishandling or user experience issues.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.utils.translation import gettext_lazy

from core.models import User

from core.models import  country, Language
from core.models import usertype,userprofile
from partner.models import coverage, jobpoc, partnerpoc, profilepartner
from rides.models import ServiceCategory

class profileForm(forms.ModelForm):
    """
    Form for creating and updating partner profiles.

    Includes widgets for enhanced UX, customizations for appearance, and validations.
    """
    # Form fields with assigned widgets and custom classes for styling
    Name = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    Address = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    Zip_Code = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    City = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    
    # A dropdown for selecting a Country with queryset sorted by Name
    Country = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'custom-select'}),
    required=True, empty_label = 'Select Country', queryset=country.objects.all().order_by('Name'))
    Language = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'custom-select'}),
    required=True, empty_label = 'Select leanguage', queryset=Language.objects.all().order_by('Name'))
    Telephone = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    ITIN = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    IBAN = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    Website = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    APP_domain = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    webwooks_suroo = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    Google_play = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    Apple_store = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    Observation = forms.Field(widget=forms.Textarea(attrs= {
        "class":"form-control", "rows":"7",
        } ),required=True)
    class Meta:
        model = profilepartner
        # Specify model fields that should be included in this form
        fields = ('Name','Address','Zip_Code','City','Website',
        'Country','Language','Telephone','ITIN','IBAN','Google_play','Apple_store',
        'APP_description','APP_domain','webwooks_suroo','Observation',)

class localForm(forms.ModelForm):
    """
    Form for adding or updating local coverage information for a partner's services.

    Provides fields to capture location and service category details.
    """
    Country = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    DistrictRegion = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    CityMunicipality = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    # Dropdown for selecting Service Categories
    ServiceCategory = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'custom-select'}),
    required=True, empty_label = 'Select Category', queryset=ServiceCategory.objects.all().order_by('Name'))
    
    class Meta:
        model = coverage
        # Define the model fields to be included in this form
        fields = ('Country','DistrictRegion',
        'CityMunicipality','ServiceCategory')

class  contactForm(forms.ModelForm):
    """
    Form for creating and editing Partner Points of Contact (POC).

    Customizes form fields with styling classes and specifies model choice fields with custom querysets.
    """
    # Dropdown for selecting titles with sorted queryset
    Category = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'custom-select'}),
    required=False, empty_label = 'Select title', queryset=jobpoc.objects.all().order_by('JobCategory'))
    Name = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    Address  = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    Zip_Code = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    Country = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'custom-select'}),
    required=True, empty_label = 'Select Country', queryset=country.objects.all().order_by('Name'))
    email = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=True)
    Telephone = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", 
        } ),required=False)
    Language1 = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'custom-select'}),
    required=True, empty_label = 'Select leanguage', queryset=Language.objects.all().order_by('Name'))
    Language2 = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'custom-select'}),
    required=False, empty_label = 'Select leanguage', queryset=Language.objects.all().order_by('Name'))
    Observation = forms.Field(widget=forms.Textarea(attrs= {
        "class":"form-control", "rows":"7",
        } ),required=False)

    class Meta:
        model = partnerpoc
        fields = ('Category','Name','Address',
        'Zip_Code','Country','Telephone',
        'email','Language1','Language2','Observation')

class SignUpForm(UserCreationForm):
    """
    Custom sign-up form for new users, extending UserCreationForm with additional fields.

    The save method is overridden to perform additional operations after saving the new user.
    """
    username =  forms.EmailField(widget=forms.TextInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("Email address"),
    } ),required=True)

    Name = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("Name"),
    } ),required=True)
    Address = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("Address"),
    } ),required=True)
    Zip_Code = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("Zip Code"),
    } ),required=True)
    City = forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("City"),
    } ),required=True)

    password1 =  forms.CharField(widget=forms.PasswordInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("Password"),
    } ))

    password2 =  forms.CharField(widget=forms.PasswordInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("Confirm Password"),
    } ))

     
    country = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'custom-select'}),
    required=True, empty_label = gettext_lazy('Select Country'), queryset=country.objects.order_by('Name'))
    

    class Meta(UserCreationForm.Meta):
        # Inherit default user fields from UserCreationForm Meta and add new ones
        
        model = User
        fields = ('username', 'password1', 'password2')
    
    @transaction.atomic
    def save(self,commit=True):
        """
        Saves the new user and creates an associated profilepartner instance.
        """
        member = super().save(commit=False)
        member.is_active = True 
        member.email_confirmed = False
        member.email=member.username
        member.save()

        Name = self.cleaned_data['Name']
        Address = self.cleaned_data['Address']
        Zip_Code = self.cleaned_data['Zip_Code']
        City = self.cleaned_data['City']
        Country = self.cleaned_data['country']

        # Add client profile
        obj = profilepartner(user=member)
        obj.Name = Name 
        obj.Address = Address 
        obj.City = City 
        obj.Zip_Code = Zip_Code 
        obj.Country = Country
        obj.Language = Country.Language  
        obj.save()

        return member        
        
        
class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with styling classes and placeholders for login fields.
    """
    # Input fields for username and password with styling and internationalized placeholders
    
    username =  forms.CharField(widget=forms.TextInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("E-mail"),
    } ))

    password =  forms.CharField(widget=forms.PasswordInput(attrs= {
        "class":"form-control", "placeholder":gettext_lazy("Password"),
    } ))

    class Meta:
        model = User
        fields = ('username', 'password')

    def confirm_login_allowed(self, user):
        """
        Custom login confirmation that checks the user's active status.
        """
        if not user.is_active:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')

