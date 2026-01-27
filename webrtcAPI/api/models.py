from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Obtém o modelo de usuário configurado

import random
import string

def generate_random_password(length=12):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for _ in range(length))

# Model to represent a conference room
class Room(models.Model):
    room_id = models.IntegerField()  # Unique room identifier
    password = models.CharField(max_length=255)  # Room password (should be stored securely)
    max_participants = models.PositiveIntegerField()  # Número máximo de participantes
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora de criação da sala
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização

    def reset_password(self):
        """Reset the room's password to a new random value."""
        self.password = generate_random_password()
        self.save()
    
    def __str__(self):
        return f'Room {self.room_id}'

# Model para representar um agendamento da sala
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')  # Sala vinculada ao agendamento
    app = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')  # Aplicação que fez o agendamento
    start_time = models.DateTimeField()  # Data e hora de início da conferência
    end_time = models.DateTimeField()  # Data e hora de término da conferência
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora da criação do agendamento
    updated_at = models.DateTimeField(auto_now=True)  # Data e hora da última atualização

    def __str__(self):
        return f'Booking {self.pk} for Room {self.room_id}'

    class Meta:
        unique_together = ('room', 'start_time', 'end_time')  # Evita duplicidade de agendamentos para a mesma sala e horário

