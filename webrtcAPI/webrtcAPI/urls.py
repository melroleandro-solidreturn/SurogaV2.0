"""
URL configuration for webrtcAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import landing_page, BookView, RoomParticipantsView, ResetRoomPasswordsView, CreateRoomView, BookRoomView, ListaSalasDisponiveisView, RoomAvailabilityCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/', ListaSalasDisponiveisView.as_view(), name='salas-disponiveis'),
    path('room/<int:room_id>/participants/', RoomParticipantsView.as_view(), name='room-participants'),
    
    path('check-room-availability/', RoomAvailabilityCheckView.as_view(), name='check-room-availability'),
    path('book/', BookView.as_view(), name='book'),
    path('book-room/', BookRoomView.as_view(), name='book-room'),
    path('create-room/', CreateRoomView.as_view(), name='create-room'),
    path('reset-room-passwords/', ResetRoomPasswordsView.as_view(), name='reset-room-passwords'),
    
    path('', landing_page, name='landing_page'),
]
