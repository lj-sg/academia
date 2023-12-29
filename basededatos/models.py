# basededatos/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15)

# Agrega los siguientes related_name
    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="user_permissions",
        related_query_name="user",
    )
