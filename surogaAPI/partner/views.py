"""
Partner Views - Suroga API

This module defines view functions and view classes for the Partner application of the Suroga API.
It includes views to handle various actions like partner login, payment and API log searches, 
client registration, handling user profiles, adding, updating and deleting partner-related records.

The views are secured with login and API-specific permissions to ensure that only authenticated 
and authorized users can access and modify partner data. They handle both form submissions and 
rendering of templates, providing necessary responses to users based on their requests.

Usage:
    - The views should be imported and included in the app's `urls.py` file to be accessible via HTTP.
    - They should be used paired with appropriate templates and forms to provide a complete user experience.

Functions:
    - Confirm views for rendering confirmation templates post-actions (login, signup)
    - Search views for querying transaction logs, API logs and other user activities
    - `CreateView`, `UpdateView`, and `DeleteView` subclasses to handle CRUD operations through class-based views

Ensure that the views adhere to the business logic and application flow. Changes should be thoroughly 
tested before deployment to maintain application stability and integrity.

Maintainer: Carlos Leandro
Last Modified: 15/3/2024
"""
from datetime import datetime, timedelta
import pytz

from django.shortcuts import render, redirect
from django.views.generic import DeleteView, CreateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
from django.urls import reverse_lazy

from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.utils.decorators import method_decorator
from django.utils.translation import activate, gettext
from django.utils import timezone

User = get_user_model()

from core.decorators import api_client_required
from partner.models import profilepartner, partnerpoc,coverage,profilepartner
from rides.models import paymentlog
from core.models import events,userloginlog
from rest_framework.authtoken.models import Token
from .forms import profileForm, localForm, contactForm, SignUpForm
from drf_api_logger.models import APILogsModel

# Create your views here.

def price_format(value,country):
    """
    Format the given value based on the currency settings of the country.

    Args:
        value: A numerical amount of money.
        country: An object of type country containing currency settings.

    Returns:
        A string representing the formatted value with the currency symbol.
    """
    Currency = country.Currency
    Value = format(value, '.2f') 

    if Currency.SymbolRight:
        Value = Value + Currency.CurrencySymbol
    else:
        Value = Currency.CurrencySymbol + Value

    return Value

@login_required(login_url="login")
@api_client_required
def change_password(request):
    """
    Process a password change request for the user.
    
    Upon successful password change, updates the session to keep the user logged in.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            ## Alert staff
            #m=MessageBoard(Sender = request.user, Code = 0, 
            #Text = "Password changed."
            #)
            #m.save()
            
            return HttpResponse(render_to_string('partner/confirm.html'))
        #else:
        #    messages.error(request, 'Please correct the error below.')
    else:

        form = PasswordChangeForm(request.user)

    return render(request, 'partner/password_change.html', {
        'form': form, 
    })


@method_decorator([login_required(login_url="login"), api_client_required], name='dispatch') 
class clientProfile(UpdateView):
    """
    A class-based view handling profile updates for partner clients.

    Performs access control checks and returns the updated profile object upon success.
    """
    model = profilepartner
    form_class = profileForm
    template_name = 'partner/profile.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Extends the base implementation to include additional context such as user data and API token.
        """

        if self.object.user != self.request.user:
            raise Http404

        if self.object.API_activated:
            key = Token.objects.get(user=self.request.user)
        else:
            key = ''

        context = super().get_context_data(**kwargs)
        context['user_type'] = 'client'
        context['user'] = self.object.user
        context['partner'] = self.object
        context['key'] = key
        context['pk'] = self.object.pk
        context['is_client'] = 1

        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #context['code'] = code
        return context
    
    def form_valid(self, form):
        """
        Logic executed when the submitted form data is valid.

        Updates the partner's profile with new data and redirects to the partner dashboard.
        """

        profile = form.save(commit=False)

        profile.save()


        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #activate(code)

        
        return redirect('/partner/')

@login_required(login_url="login")
@api_client_required
def confirm(request):
    """
    View to display a confirmation page to the user.

    This view is decorated with 'login_required' to ensure that only
    authenticated users can access it, and 'api_client_required' to
    check for API client permissions.
    """
    return HttpResponse(render_to_string('partner/confirm.html'))

@method_decorator([login_required(login_url="login"), api_client_required], name='dispatch') 
class ContactsAdd(CreateView):
    """
    A view for adding new Point of Contact (POC) records to a partner's profile.

    'login_required' and 'api_client_required' enforce the need for authenticated users with proper API permissions.
    """
    model = partnerpoc
    form_class = contactForm
    template_name = 'partner/addcontact.html'
    success_url = '/'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['user_type'] = 'client'
        
        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #context['code'] = code
        return context
    
    def form_valid(self, form):
        """
        Logic to execute when the contact form is valid.

        Sets the user associated with the contact and saves the contact instance.
        Then redirects to the confirmation page.
        """

        contact = form.save(commit=False)
        contact.user = self.request.user

        # Saving contact and redirecting to the confirmation page.
        contact.save()


        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #activate(code)

        return redirect('/partner/confirm')

@method_decorator([login_required(login_url="login"), api_client_required], name='dispatch') 
class ContactsDelete(DeleteView):
    """
    View for deleting a Point of Contact (POC) associated with a partner's profile.
    
    Enforces access constraints to ensure that only the owner can delete the POC.
    """
    model = partnerpoc
    template_name = 'partner/deletecontact.html'
    success_url = '/'

    def get_context_data(self, **kwargs):

        # Ensure the user requesting deletion is the owner of the POC.
        if self.object.user != self.request.user:
            raise Http404

        context = super().get_context_data(**kwargs)
        context['user_type'] = 'client'
        context['pk'] = self.object.pk

        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #context['code'] = code
        return context

@method_decorator([login_required(login_url="login"), api_client_required], name='dispatch') 
class ContactUpdate(UpdateView):
    """
    View for updating an existing Point of Contact (POC) for a partner's profile.

    Enforces access controls and facilitates updates to POC information with validation.
    """
    model = partnerpoc
    form_class = contactForm
    template_name = 'partner/updatecontact.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        # Ensure that the user attempting to update is the owner of the POC.
        if self.object.user != self.request.user:
            raise Http404

        context = super().get_context_data(**kwargs)
        context['user_type'] = 'client'
        context['pk'] = self.object.pk

        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #context['code'] = code
        return context
    
    def form_valid(self, form):
        """
        Executes logic when the form to update a partner's contact is valid.

        Saves the updated POC data and returns a confirmation response.
        """

        contact = form.save(commit=False)

        # Updating contact and rendering confirmation page.
        contact.save()


        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #activate(code)

        
        return HttpResponse(render_to_string('partner/confirm.html'))

@method_decorator([login_required(login_url="login"), api_client_required], name='dispatch') 
class LocalAdd(CreateView):
    """
    A class-based view to handle the addition of new local coverage areas for partners.

    Requires user authentication and specific API client permissions to proceed with the addition of coverage areas.
    """
    model = coverage
    form_class = localForm
    template_name = 'partner/addlocal.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Provides additional context data to the local coverage addition template.
        """
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'client'
        
        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #context['code'] = code
        return context
    
    def form_valid(self, form):
        """
        Handles the processing of valid forms for adding new local coverage areas.
        """
        local = form.save(commit=False)

        # Set the current user on new local area, ensure all necessary information is saved, handle language preference...
        local.user = self.request.user

        local.save()


        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #activate(code)

        return redirect('/partner/confirm')

@method_decorator([login_required(login_url="login"), api_client_required], name='dispatch') 
class LocalDelete(DeleteView):
    """
    A class-based view for partners to delete local coverage areas.

    Partners should only be able to delete their own coverage areas.
    """
    model = coverage
    template_name = 'partner/deletelocal.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Extends basic context data with additional checks and information like user type.
        """

        # Prevent deletion if the coverage area is not owned by current user...
        if self.object.user != self.request.user:
            raise Http404

        context = super().get_context_data(**kwargs)
        context['user_type'] = 'client'
        context['pk'] = self.object.pk

        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #context['code'] = code
        return context

@method_decorator([login_required(login_url="login"), api_client_required], name='dispatch') 
class LocalUpdate(UpdateView):
    """
    Class-based view to handle updates to existing local coverage areas for partners.

    Verification ensures that only the owner partner is able to update their coverage area details.
    """
    model = coverage
    form_class = localForm
    template_name = 'partner/updatelocal.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Augments the context for the update coverage template with user-specific data.
        """


        # Check if the coverage area belongs to the current user before allowing an update...
        if self.object.user != self.request.user:
            raise Http404

        context = super().get_context_data(**kwargs)
        context['user_type'] = 'client'
        context['pk'] = self.object.pk

        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #context['code'] = code
        return context
    
    def form_valid(self, form):
        """
        Logic executed after the form for updating local coverage is validated.
        """
        local = form.save(commit=False)

        local.save()


        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #activate(code)

        
        return HttpResponse(render_to_string('partner/confirm.html'))


@login_required(login_url="login")
@api_client_required
def viewTransation(request, *args, **kwargs):
    """
    View a detailed page for a single payment transaction.

    Args:
        request: The HTTP request object.
        pk: The primary key of the payment transaction to view.

    Returns:
        An HttpResponse with the rendered transaction detail template.
    """
    pk = int(kwargs['pk'])

    item = paymentlog.objects.get(pk=pk)

    # Ensure the requesting user is the one associated with the payment log entry
    if item.user != request.user:
        raise Http404

    # Render the transaction detail page and return the response.
    data ={
        'item':item,
        }
    return HttpResponse(render_to_string('partner/viewTransation.html',data))

@login_required(login_url="login")
@api_client_required
def viewLogin(request, *args, **kwargs):
    """
    View a detailed page for a single login log entry.

    Args:
        request: The HTTP request object.
        pk: The primary key of the login log entry to view.

    Returns:
        An HttpResponse with the rendered login log detail template.
    """
    pk = int(kwargs['pk'])

    item = userloginlog.objects.get(pk=pk)
    
    # Verify that the login log entry belongs to the requesting user.
    if item.user != request.user:
        raise Http404

    data ={
        'item':item,
        }
    return HttpResponse(render_to_string('partner/viewLogin.html',data))

@login_required(login_url="login")
@api_client_required
def viewRequest(request, *args, **kwargs):
    """
    Display a detailed page for a single API request log entry.

    Args:
        request: The HTTP request object.
        pk: The primary key of the API request log entry to view.

    Returns:
        An HttpResponse with the rendered request log detail template.
    """
    pk = int(kwargs['pk'])

    item = APILogsModel.objects.get(pk=pk)

    # Ensure the request log entry is associated with the current user.
    if item.user != request.user:
        raise Http404

    data ={
        'item':item,
        }
    return HttpResponse(render_to_string('partner/viewRequest.html',data))


@login_required(login_url="login")
@api_client_required
def searchTransaction(request, *args, **kwargs):
    """
    Search and display a list of payment transactions within a specified date range.

    Args:
        request: The HTTP request object.
        start: Start date for the search query.
        end: End date for the search query.

    Returns:
        An HttpResponse with the rendered search results template.
    """
    start = kwargs['start']
    end = kwargs['end']
    
    partner = profilepartner.objects.get(user=request.user)
    timezone = pytz.timezone(partner.Country.time_zone.TimeZone)

    start = datetime.strptime(start, '%Y-%m-%d')
    startDate = timezone.localize(start)

    end = datetime.strptime(end, '%Y-%m-%d')
    endDate = timezone.localize(end)
    
    payment = paymentlog.objects.filter(user=request.user,RegistrationDate__gte=startDate, RegistrationDate__lte=endDate)
    PaymentLog=[]
    for pay in payment:
        PaymentLog.append([pay.pk,pay.RegistrationDate,pay.OperationType,pay.SettlementDate, pay.Ride.pk,pay.Booking.pk,price_format(pay.Value,partner.Country)])
    
    data ={
        'PaymentLog':PaymentLog,
        }
    return HttpResponse(render_to_string('partner/searchTransaction.html',data))

@login_required(login_url="login")
@api_client_required
def searchRequests(request, *args, **kwargs):
    """
    Search and display a list of API request logs within a specified date range.

    Args:
        request: The HTTP request object.
        start: Start date for the search query.
        end: End date for the search query.

    Returns:
        An HttpResponse with the rendered search results template.
    """
    start = kwargs['start']
    end = kwargs['end']
    
    partner = profilepartner.objects.get(user=request.user)
    timezone = pytz.timezone(partner.Country.time_zone.TimeZone)

    start = datetime.strptime(start, '%Y-%m-%d')
    startDate = timezone.localize(start)

    end = datetime.strptime(end, '%Y-%m-%d')
    endDate = timezone.localize(end)

    requests = APILogsModel.objects.filter(user=request.user,added_on__gte=startDate, added_on__lte=endDate)
    
    EventLog=[]
    for event in requests:
        EventLog.append([event.pk,event.added_on,event.method,event.api,event.client_ip_address])

    data ={
        'EventLog':EventLog,
        }
    return HttpResponse(render_to_string('partner/searchRequests.html',data))

@login_required(login_url="login")
@api_client_required
def searchLogin(request, *args, **kwargs):
    """
    Searches and displays login logs based on the specified date range.

    Args:
        request: The HTTP request object.
        start: Start date for the search query.
        end: End date for the search query.

    Returns:
        An HttpResponse with the list of login logs within the date range.
    """
    start = kwargs['start']
    end = kwargs['end']
    
    partner = profilepartner.objects.get(user=request.user)
    timezone = pytz.timezone(partner.Country.time_zone.TimeZone)

    start = datetime.strptime(start, '%Y-%m-%d')
    startDate = timezone.localize(start)

    end = datetime.strptime(end, '%Y-%m-%d')
    endDate = timezone.localize(end)

    logs = userloginlog.objects.filter(user=request.user,RegistrationDate__gte=startDate, RegistrationDate__lte=endDate)
    
    AccessLog=[]
    for access in logs:
        AccessLog.append([access.RegistrationDate,access.IP,access.local, access.country])

    data ={
        'AccessLog':AccessLog,
        }
    return HttpResponse(render_to_string('partner/searchLogin.html',data))

@login_required(login_url="login")
@api_client_required
def ClientDashboard(request, *args, **kwargs):
    """
    Renders the partner client's dashboard with recent log information.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered template response with the complete dashboard context.
    """
    # Dashboard data preparation and context setup goes here...
    end   = datetime.today()
    start = end - timedelta(days=8)
    
    enddate   = end.strftime("%Y-%m-%d")
    startdate = start.strftime("%Y-%m-%d")

    partner = profilepartner.objects.get(user=request.user)
    
    if partner.API_activated:
        key = Token.objects.get(user=request.user)
    else:
        key = ''
    
    logs = userloginlog.objects.filter(user=request.user,RegistrationDate__gte=start, RegistrationDate__lte=end)
    requests = APILogsModel.objects.filter(user=request.user,added_on__gte=start, added_on__lte=end)
    payment = paymentlog.objects.filter(user=request.user,RegistrationDate__gte=start, RegistrationDate__lte=end)
    cover = coverage.objects.filter(user=request.user)
    poc = partnerpoc.objects.filter(user=request.user)
    
    AccessLog=[]
    for access in logs:
        AccessLog.append([access.pk,access.RegistrationDate,access.IP,access.local, access.country])

    EventLog=[]
    for event in requests:
        EventLog.append([event.pk,event.added_on,event.method,event.api,event.client_ip_address])

    PaymentLog=[]
    for pay in payment:
        PaymentLog.append([pay.pk,pay.RegistrationDate,pay.OperationType,pay.SettlementDate, pay.Ride.pk,pay.Booking.pk,price_format(pay.Value,partner.Country)])

    AppCover=[]
    for local in cover:
        AppCover.append([local.pk,local.Country,local.DistrictRegion, local.CityMunicipality,local.ServiceCategory])

    POCs=[]
    for person in poc:
        POCs.append([person.pk,person.Category,person.Name,person.email, person.Telephone,person.Address,person.Zip_Code,person.Country])

    data ={
        'is_anonymous': 0,
        'is_client': 1, 
        'user': request.user, 
        'partner':partner, 
        'startdate':startdate,
        'enddate':enddate,
        'key': key,
        'AccessLog': AccessLog, 
        'EventLog': EventLog,
        'PaymentLog':PaymentLog,
        'AppCover':AppCover,
        'POCs':POCs,
        }

    return render(request, 'partner/dashboard.html', data) 

def confirmLogin(request):
    """
    Renders a confirmation page upon successful login.

    Returns:
        An HttpResponse with the confirmation template.
    """
    # Render and return the login confirmation page...
    return HttpResponse(render_to_string('partner/confirmLogin.html'))

# Client signup
class ClientSignUp(CreateView):
    """
    Handles the client sign-up process.
    
    Upon successful sign-up, the user is redirected to a confirmation page.
    """
    model = User
    form_class = SignUpForm
    template_name = 'partner/clientsignup.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Adds additional context for rendering the client sign-up template.

        Returns:
            The extended context.
        """
        # Add context such as user type...        
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'partner'

        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        #activate(code)

        #context['code'] = code

        return context

    def form_valid(self, form):
        """
        Processes a valid sign-up form submission.

        Returns:
            A redirect response to a signup confirmation page.
        """
        # Sign-up form processing and confirmation logic goes here...
        user = form.save()

        #user.set_password(user.password)
        #user.save()

        #try:
        #    code = self.request.session['code']
        #except KeyError:
        #    if self.request.user.Language.Code:
        #        code = self.request.user.Language.Code
        #    else:
        #        code = 'en'

        current_site = get_current_site(self.request)
        subject = gettext('Suroga email account confirmation.')
        next = self.request.session.get('next', '/')
        
        #message = render_to_string('client/email_confirmation_'+code+'.html', {
        #    'username': user.username,
        #    'domain': current_site.domain,
        #    'port': self.request.get_port(),
        #    'next': next,
        #    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #'token': account_activation_token.make_token(user),
        #})

       
        #msg = EmailMessage(subject,message, to=[user.email])

        
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        #try:
        #    msg.send()
        #except ConnectionRefusedError:
            # Alert staff
        #    m=MessageBoard(Sender = user, Code = 0, Text = "Connection Refused Error.")
        #    m.save()


        return HttpResponse(render_to_string('partner/confirmSignup.html'))
