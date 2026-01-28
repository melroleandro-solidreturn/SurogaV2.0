"""
Partner Application URL Configuration - Suroga API

This module outlines the URL patterns for the Partner application, responsible for facilitating
web requests to appropriate views related to partner management and operations within the Suroga API.

By defining these patterns, the application can serve different web pages and API endpoints,
effectively mapping URL routes to the functions that handle requests for those routes.

Usage:
    - Include these URL patterns in the project's main `urls.py` file using Django's `include()` function.
    - Use the `name` parameter to reverse these URLs in templates and views for consistent URL referencing.

Patterns:
    - Authentication views are provided by Django's built-in auth views with additional customization.
    - Sign-up, login, profile management, and other functionalities relevant to partner management are routed here.
    - Custom views for specific partner interactions are defined with clear, actionable names.

References:
    - Django URL dispatcher: https://docs.djangoproject.com/en/4.0/topics/http/urls/
    - Django Authentication Views: https://docs.djangoproject.com/en/4.0/topics/auth/default/#module-django.contrib.auth.views

Ensure that all views are properly imported and available for creating URL patterns, and that the
named URL patterns match those used in the rest of the application for consistency.

Maintainer: Carlos Leandro
Last Modified: 15/3/2024
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from django.contrib.auth import views as auth_views
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view

from core import views as coreviews
from partner import forms as partnerforms
from partner import views as partnerviews

app_name = 'partner'

urlpatterns = [
    # Change password view for a partner
    url(r'^password/$', partnerviews.change_password, name='password_change'),
    
    # Logout view which redirects to the home page after logging out
    url(r'^logout/$',auth_views.LogoutView.as_view(next_page = '/'), name='logout'),
    
    # Signup view for new clients
    url(r'^signup/$',partnerviews.ClientSignUp.as_view(), name='client_signup'),
    
    # Login view with a custom authentication form and a language code in the context
    url(r'^login/$', auth_views.LoginView.as_view(template_name = 'partner/clientlogin.html',
        authentication_form = partnerforms.CustomAuthenticationForm, extra_context = {'code':'en'}), name='login'),
    
    # Confirm login attempt view
    url(r'^confirmLogin/$', partnerviews.confirmLogin, name='confirmLogin'),
    
    # Profile update view for a client with a specific primary key (pk)
    path('clientProfile/<int:pk>/', partnerviews.clientProfile.as_view(), name='profile-update'),  
    
    # View for updating, adding, and deleting contacts
    path('contactUpdate/<int:pk>/',partnerviews.ContactUpdate.as_view(), name='contact-update'),
    path('contactAdd/',partnerviews.ContactsAdd.as_view(), name='contact-add'),
    path('contactDelete/<int:pk>/', partnerviews.ContactsDelete.as_view(), name='contact-delete'),
    
    # View for updating, adding, and deleting location information
    path('localUpdate/<int:pk>/',partnerviews.LocalUpdate.as_view(), name='local-update'),
    path('localAdd/',partnerviews.LocalAdd.as_view(), name='local-add'),
    path('localDelete/<int:pk>/', partnerviews.LocalDelete.as_view(), name='local-delete'),
    
    # Confirm view for account confirmation operations
    url(r'^confirm/$', partnerviews.confirm, name='confirm'),
    
    # Search and view transactions, requests, and login data within a given date range
    path('searchTransactions/<str:start>/<str:end>/', partnerviews.searchTransaction, name='searchTransaction'),
    path('searchRequests/<str:start>/<str:end>/', partnerviews.searchRequests, name='searchRequests'),
    path('searchLogin/<str:start>/<str:end>/', partnerviews.searchLogin, name='searchLogin'),
    path('viewTransation/<int:pk>/', partnerviews.viewTransation, name='viewTransation'),
    path('viewRequest/<int:pk>/', partnerviews.viewRequest, name='viewRequest'),
    path('viewLogin/<int:pk>/', partnerviews.viewLogin, name='viewLogin'),
    
    # The main dashboard view for clients
    path('',partnerviews.ClientDashboard, name='client_dashboard'),
]