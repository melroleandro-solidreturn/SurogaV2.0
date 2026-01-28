"""
Rides Application URL Configuration

This module defines the URL patterns for the Rides application within the Suroga API project.
It specifies the mappings between URL paths, views, and actions for handling ride-related resources,
including registration, booking, stock management, and messaging functionalities.

By associating views with specific paths, the Django application can route incoming HTTP requests to the appropriate view logic, 
enabling RESTful interaction with the backend models via the Django REST Framework's viewsets.

The configuration supports both standard CRUD actions generated through routers and custom actions defined within each viewset,
reflecting the needs and the flow of the Rides application logic.

Usage:
    - Used by Django to match requested URLs to appropriate viewsets according to the provided routing patterns.
    - Centralized location to look up URL paths and their corresponding view logic for the application's endpoints.

References:
    - Django URL dispatcher: https://docs.djangoproject.com/en/4.0/topics/http/urls/
    - Django REST Framework routers: https://www.django-rest-framework.org/api-guide/routers/

This file should be updated with care, as changes could alter the public API surface and impact client applications.
Changes should be tested to confirm expected behavior.

Maintainer: Carlos Leandro
Last Modified: 15/3/2014
"""
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from rides.views import messageViewSet,stockViewSet, ratingViewSet,servicecategoryViewSet,ridetypeViewSet,rideViewSet
from rides.views import  bookingViewSet

app_name = 'rides'

# Define URL patterns for rides using rideViewSet class
ride_list = rideViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

ride_detail = rideViewSet.as_view({
    'get': 'retrieve',
    'post': 'update'
})

# Define URL patterns for bookings using bookingViewSet class
booking_list = bookingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

booking_detail = bookingViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
})

# Define URL patterns for stock items using stockViewSet class
stock_list = stockViewSet.as_view({
    'get': 'list',
})

stock_detail = stockViewSet.as_view({
    'get': 'retrieve',
})

# Define URL patterns for messages using messageViewSet class
messages_list = messageViewSet.as_view({
    'get': 'list',
})

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'rating', ratingViewSet) # URL for rating viewset
router.register(r'ride-category', servicecategoryViewSet) # URL for service category viewset
router.register(r'ride-type', ridetypeViewSet)  # URL for ride type viewset
#router.register(r'registration', rideViewSet)
#router.register(r'booking', bookingViewSet)
#router.register(r'stock', stockViewSet)
#router.register(r'messages', messageViewSet)

# URL patterns for the Ride resource with list and detail views, along with custom actions.
urlpatterns = [
    
    # URL pattern for listing all rides or creating a new ride
    path('registration/', ride_list, name='ride-list'), 
    
    # URL pattern for retrieving, updating, or deleting a specific ride based on its primary key
    path('registration/<int:pk>/', ride_detail, name='ride-detail'),
    
    # URL pattern for canceling a specific ride
    path('registration/<int:pk>/cancel', rideViewSet.as_view({'get': 'cancel'}), name='ride-cancel'),
    
    # URL pattern for deleting a specific ride
    path('registration/<int:pk>/delete', rideViewSet.as_view({'get': 'delete'}), name='ride-delete'),
    
    # URL pattern for deleting a specific ride
    path('registration/<int:pk>/click', rideViewSet.as_view({'get': 'click'}), name='ride-click'),

    # URL pattern for deleting a specific ride
    path('registration/<int:pk>/booked', rideViewSet.as_view({'get': 'booked'}), name='ride-booked'),

    # URL for generating a payment link for a specific ride
    #path('registration/<int:pk>/payment_link', rideViewSet.as_view({'get': 'paymentlink'}), name='ride-payment'),
    
    # URL for closing a ride
    path('registration/<int:pk>/close', rideViewSet.as_view({'get': 'close'}), name='ride-close'),
    
    # URL pattern for listing all bookings or creating a new booking
    path(r'booking/', booking_list, name='booking-list'),
    
    # URL pattern for retrieving, updating, or deleting a specific booking
    path('booking/<int:pk>/', booking_detail, name='booking-detail'),
    
    # URL pattern for sending a message related to a booking
    path('booking/<int:pk>/send', bookingViewSet.as_view({'get': 'send'}), name='booking-send'),
    
    # More URL patterns for custom actions related to bookings, such as cancel, delete, handle extras, dispute, payment link, etc.

    path('booking/<int:pk>/cancel', bookingViewSet.as_view({'get': 'cancel'}), name='booking-cancel'),
    path('booking/<int:pk>/delete', bookingViewSet.as_view({'get': 'delete'}), name='booking-delete'),
    path('booking/<int:pk>/extra_costs', bookingViewSet.as_view({'get': 'extra_costs'}), name='booking-extras'),
    path('booking/<int:pk>/dispute', bookingViewSet.as_view({'get': 'dispute'}), name='booking-dispute'),
    path('booking/<int:pk>/payment_link', bookingViewSet.as_view({'get': 'paymentlink'}), name='booking-payment'),
    path('booking/<int:pk>/dashboards', bookingViewSet.as_view({'get': 'dashoards'}), name='booking-dashoards'),
    path('booking/<int:pk>/client_classification', bookingViewSet.as_view({'get': 'client_classification'}), name='booking-client-rank'),
    path('booking/<int:pk>/surrogate_classification', bookingViewSet.as_view({'get': 'surrogate_classification'}), name='booking-agent-rank'),
    path('booking/<int:pk>/ride_start', bookingViewSet.as_view({'get': 'ride_start'}), name='booking-strat'),
    path('booking/<int:pk>/ride_end', bookingViewSet.as_view({'get': 'ride_end'}), name='booking-end'),
    path('booking/<int:pk>/ride_close', bookingViewSet.as_view({'get': 'close'}), name='booking-close'),
    
    
    # URL pattern for listing stock items
    path('stock/', stock_list, name='stock-list'),
    
    # URL pattern for retrieving a specific stock item details
    path('stock/<int:pk>/', stock_detail, name='stock-detail'),
    
    # URL pattern for selecting or unselecting a stock item
    path('stock/<int:pk>/select',stockViewSet.as_view({'get': 'selected'}), name='stock-select'),
    path('stock/<int:pk>/unselect',stockViewSet.as_view({'get': 'unselected'}), name='stock-unselect'),
    
    # URL pattern for listing messages
    path('messages/', messages_list, name='messages-detail'),
    
    # URL pattern for custom actions on messages, such as mark as read, delete, or report as abuse
    path('messages/<int:pk>/readed', messageViewSet.as_view({'get': 'readed'}), name='message-readed'),
    path('messages/<int:pk>/delete', messageViewSet.as_view({'get': 'delete'}), name='message-delete'),
    path('messages/<int:pk>/abuse', messageViewSet.as_view({'get': 'abuse'}), name='message-abuse'),
    
    # Including URLs from router for DRF ViewSets
    path('', include(router.urls)),
]