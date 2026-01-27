from rest_framework import serializers
from .models import Room, Booking  # Assuming your model is called 'Sala'

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_id', 'created_at', 'updated_at']  # Choose the fields to expose
        read_only_fields = ['room_id', 'created_at', 'updated_at']  # Avoid exposing access password if necessary

class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_id', 'password']  # Return room_id and password
        read_only_fields = ['password']  # Optionally, you might not want to expose the password

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['room', 'start_time', 'end_time']  # Fields that will be used for booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['room', 'start_time', 'end_time']  # Fields that will be used for booking

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_id', 'password', 'max_participants']  # Fields needed for room creation