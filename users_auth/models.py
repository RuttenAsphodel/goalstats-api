from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('SUPER_ADMIN', 'Super Administrador'),
        ('ADMIN', 'Administrador'),
        ('COACH', 'Entrenador'),
        ('PLAYER', 'Jugador'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='PLAYER')