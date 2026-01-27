import requests
import random
import string
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Room, Booking, generate_random_password
from .serializers import RoomSerializer, BookingSerializer, SalaSerializer, RoomAvailabilitySerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
import uuid
from api.janus_calls import createTask, editTask, destroyTask, activateTask, blockTask, countTask


def create_room_in_janus(room_id,MettingID, MettingPIN, BlockingPIN):

    # Send task
    createTask(room_id, MettingPIN, BlockingPIN,  False, MettingID, meeting)

def generate_random_password(length=10):
    """Gera uma senha aleatória com o tamanho especificado."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def update_room_password(room_id):
    # Fetch the room from the database
    room = Room.objects.get(room_id=room_id)
    
    # Generate a new random password
    new_password = generate_random_password()
    
    # Update the password in the Django model
    room.password = new_password
    room.save()

    # Update the password in the Janus server
    url = f"{settings.JANUS_URL}/janus"
    
    # Gerar um ID de transação único
    transaction_id = str(uuid.uuid4())

    # Solicitar para editar a sala e mudar a senha
    edit_room_request = {
        "janus": "message",
        "body": {
            "request": "edit",
            "room": room_id,
            "secret": room.password,  # Current password for authentication
            "new_secret": new_password,  # New password
            "permanent": False  # If True, the change will be permanent in the Janus configuration file
        },
        "transaction": transaction_id,
        "apisecret": settings.JANUS_KEY
    }

    # Enviar a solicitação para o Janus
    response = requests.post(url, json=edit_room_request)
    edit_room_response = response.json()

    # Process the response
    if edit_room_response.get("janus") == "success":
        print(f"Password for room {room_id} updated successfully to {new_password}")
    else:
        print(f"Failed to update password for room {room_id}: {edit_room_response.get('error')}")


class ListaSalasDisponiveisView(generics.ListAPIView):
    queryset = Room.objects.all()  # Lista todas as salas
    serializer_class = SalaSerializer
    permission_classes = [IsAuthenticated]  # Garante que o usuário esteja autenticado
    
    def list(self, request, *args, **kwargs):
        '''
        # URL do Janus
        url = f"{settings.JANUS_URL}/janus"
        
        # Solicitar a lista de salas
        list_rooms_request = {
            "janus": "message",
            "body": {
                "request": "list"
            },
            "transaction": str(uuid.uuid4()),  # Gerar um ID de transação único
            "apisecret": settings.JANUS_KEY
        }

        response = requests.post(url, json=list_rooms_request)
        
        list_rooms_response = response.json()
        
        if list_rooms_response.get("janus") == "success":
            janus_rooms = list_rooms_response.get("list", [])
        else:
            return Response({"error": "Failed to list VideoRooms from Janus"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        '''
        
        # Fetch the list of rooms from the Django model
        django_rooms = Room.objects.all()
        
        # Compare and synchronize the rooms
        #self.synchronize_rooms(django_rooms, janus_rooms)
        
        # Return the list of rooms from the Django model
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)
    
    def synchronize_rooms(self, django_rooms, janus_rooms):
        # Create a set of room IDs from Janus
        janus_room_ids = {room['room'] for room in janus_rooms}
        
        # Create a set of room IDs from Django
        django_room_ids = {room.room_id for room in django_rooms}
        
        # Find rooms that are in Janus but not in Django
        missing_in_django = janus_room_ids - django_room_ids
        for room_id in missing_in_django:
            # Create a new room in Django
            room_data = next(room for room in janus_rooms if room['room'] == room_id)
            Room.objects.create(
                room_id=room_data['room'],
                password=room_data.get('secret', ''),
                max_participants=room_data.get('publishers', 0)
            )
        
        # Find rooms that are in Django but not in Janus
        missing_in_janus = django_room_ids - janus_room_ids
        for room_id in missing_in_janus:
            # Delete the room from Django
            Room.objects.filter(room_id=room_id).delete()
        
        # Update existing rooms in Django
        for django_room in django_rooms:
            janus_room = next((room for room in janus_rooms if room['room'] == django_room.room_id), None)
            if janus_room:
                django_room.password = janus_room.get('secret', '')
                django_room.max_participants = janus_room.get('publishers', 0)
                django_room.save()
        
                


class RoomAvailabilityCheckView(generics.GenericAPIView):
    serializer_class = RoomAvailabilitySerializer
    permission_classes = [IsAuthenticated]  # Garante que o usuário esteja autenticado


    def get(self, request, *args, **kwargs):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not start_time or not end_time:
            return Response({'error': 'Both start_time and end_time must be provided.'}, status=400)

        try:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)
        except ValueError:
            return Response({'error': 'Invalid date format. Use ISO 8601 format.'}, status=400)

        # Find rooms that are not booked during the given time range
        available_rooms = Room.objects.exclude(
            bookings__start_time__lt=end_time,
            bookings__end_time__gt=start_time
        ).distinct()

        if not available_rooms.exists():
            raise NotFound('No rooms available during the specified time range.')

        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)

class BookView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        if not start_time or not end_time:
            return Response({'error': 'start_time, and end_time must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)
        except ValueError:
            return Response({'error': 'Invalid date format. Use ISO 8601 format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the room exists
        try:
            rooms = Room.objects.all()
        except Room.DoesNotExist:
            return Response({'error': 'Rooms not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check for booking conflicts
        free_room=False
        for room in rooms:
            conflicting_bookings = Booking.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if not conflicting_bookings.exists():
                free_room = True
                break
        if not free_room:
            # create room
            while True:
                room_id = random.randint(10000, 99999)
                if not Room.objects.filter(room_id=room_id).exists():
                    break
            
            # Generate a random password
            password = generate_random_password()
            
            # Set the room_id and password
            serializer.save(room_id=room_id, password=password, max_participants=2)

            # Create the room in the Janus server
            create_room_in_janus(room_id, password)

        print(room,request.user,start_time,end_time)        
        # Create booking
        booking = Booking.objects.create(
            room=room,
            app = request.user,
            start_time=start_time,
            end_time=end_time
        )

        return Response({'status': 'OK','room': room.room_id, 'pw': room.password}, status=status.HTTP_201_CREATED)

class BookRoomView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        room_id = request.data.get('room')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        if not room_id or not start_time or not end_time:
            return Response({'error': 'room, start_time, and end_time must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)
        except ValueError:
            return Response({'error': 'Invalid date format. Use ISO 8601 format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the room exists
        try:
            room = Room.objects.get(room_id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check for booking conflicts
        conflicting_bookings = Booking.objects.filter(
            room=room,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if conflicting_bookings.exists():
            return Response({'error': 'Room is already booked during the specified time range.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create booking
        booking = Booking.objects.create(
            room=room,
            app = request.user,
            start_time=start_time,
            end_time=end_time
        )

        return Response({'status': 'OK','room': room.room_id, 'pw': room.password}, status=status.HTTP_201_CREATED)

class CreateRoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Generate a unique 5-digit room_id
        while True:
            room_id = random.randint(10000, 99999)
            if not Room.objects.filter(room_id=room_id).exists():
                break
        
        # Generate a random password
        password = generate_random_password()
        
        # Set the room_id and password
        serializer.save(room_id=room_id, password=password, max_participants=2)

        # Create the room in the Janus server
        create_room_in_janus(room_id, password)


class ResetRoomPasswordsView(APIView):
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        now = timezone.now()

        # Find rooms that are not currently booked for future dates
        rooms_to_reset = Room.objects.filter(
            Q(booking__end_time__lte=now) | Q(booking__isnull=True)
        ).distinct()

        # Reset passwords for all rooms found
        for room in rooms_to_reset:
            # Generate a new random password
            new_password = room.reset_password()
            
            # Update the password in the Janus server
            self.update_password_in_janus(room.room_id, new_password)

        return Response({'status': 'Passwords reset for all applicable rooms.'}, status=status.HTTP_200_OK)

    def update_password_in_janus(self, room_id, new_password):
        # URL do Janus
        url = f"{settings.JANUS_URL}/janus"

        # Request to edit the room and change the password
        edit_room_request = {
            "janus": "message",
            "body": {
                "request": "edit",
                "room": room_id,
                "secret": new_password,  # New password
                "permanent": False  # If True, the change will be permanent in the Janus configuration file
            },
            "transaction": str(uuid.uuid4()),  # Gerar um ID de transação único
            "apisecret": settings.JANUS_KEY
        }

        # Enviar a solicitação para o Janus
        response = requests.post(url, json=edit_room_request)
        edit_room_response = response.json()

        # Process the response
        if edit_room_response.get("janus") == "success":
            print(f"Password for room {room_id} updated successfully to {new_password}")
        else:
            print(f"Failed to update password for room {room_id}: {edit_room_response.get('error')}")


class RoomParticipantsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        room_id = kwargs.get('room_id')

        # URL do Janus
        url = f"{settings.JANUS_URL}/janus"

        # Request to list all participants in the room
        list_participants_request = {
            "janus": "message",
            "body": {
                "request": "listparticipants",
                "room": room_id
            },
            "transaction": str(uuid.uuid4()),  # Gerar um ID de transação único
            "apisecret": settings.JANUS_KEY
        }

        # Enviar a solicitação para o Janus
        print(url,list_participants_request)
        response = requests.post(url, json=list_participants_request)
        print(response)
        list_participants_response = response.json()

        # Process the response
        if list_participants_response.get("janus") == "success":
            participants = list_participants_response.get("participants", [])
            participant_count = len(participants)
            return Response({"room_id": room_id, "participant_count": participant_count})
        else:
            return Response({"error": "Failed to list participants in room"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def landing_page(request):
    return render(request, 'landing_page.html')