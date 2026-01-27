import random

from django.contrib import admin
from .models import Room, Booking, generate_random_password
from django.utils import timezone
from django.db.models import Q

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'password', 'max_participants', 'created_at', 'updated_at',)
    
    # Custom action to create a new room
    actions = ['create_new_room','reset_passwords']

    def create_new_room(self, request, queryset):
        while True:
            room_id = random.randint(10000, 99999)
            if not Room.objects.filter(room_id=room_id).exists():
                break
        
        # Generate a random password
        password = generate_random_password()
        
        # Set the room_id and password
        new_room = Room(
            room_id=room_id,
            password=password,
            max_participants=2
        )

        # Save the new room to the database
        new_room.save()


    create_new_room.short_description = "Create a new room"

    def reset_passwords(self, request, queryset):
        now = timezone.now()

        # Find rooms that are not currently booked for future dates
        rooms_to_reset = Room.objects.filter(
            Q(bookings__isnull=True) |
            Q(bookings__end_time__lt=now)
        ).exclude(
            bookings__start_time__gte=now
        ).distinct()

        # Reset passwords for all rooms found
        for room in rooms_to_reset:
            room.reset_password()

    reset_passwords.short_description = "Reset passwords"
    


admin.site.register(Room, RoomAdmin)

class BookingAdmin(admin.ModelAdmin):
	list_display = (
    'pk',
    'room',
    'app',
    'start_time',
    'end_time',
    'created_at',
    'updated_at',
    )
admin.site.register(Booking,BookingAdmin)