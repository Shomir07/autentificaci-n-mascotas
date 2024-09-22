from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings  # Para obtener el CustomUser definido en settings.py

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Añadimos related_name para evitar el conflicto
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Añadimos related_name para evitar el conflicto
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

class Card(models.Model):

    title = models.CharField(max_length=255, help_text="Título de la tarjeta")
    description = models.TextField(help_text="Descripción detallada de lo que representa la tarjeta.")
    image = models.ImageField(upload_to='pictures/', blank=True, null=True, help_text="Imagen asociada a la tarjeta.")

    class Meta:
        verbose_name = "Tarjeta"
        verbose_name_plural = "Tarjetas"
        ordering = ['title']  # Las tarjetas se ordenarán alfabéticamente por título.

    def __str__(self):
        return self.title


class ProfileImage(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='profile_image',
        help_text="Usuario al que pertenece esta imagen de perfil."
    )
    image = models.ImageField(upload_to='icons/profiles_random/', blank=True, null=True, help_text="Imagen de perfil del usuario.")

    class Meta:
        verbose_name = "Imagen de Perfil"
        verbose_name_plural = "Imágenes de Perfil"

    def __str__(self):
        return f"Imagen de perfil para {self.user.username}"


class AnimalModule(models.Model):

    name = models.CharField(max_length=255, help_text="Nombre del módulo")
    description = models.TextField(help_text="Descripción detallada de las funcionalidades de este módulo.")

    class Meta:
        verbose_name = "Módulo de Animales"
        verbose_name_plural = "Módulos de Animales"
        ordering = ['name']  # Ordenar por nombre alfabéticamente.

    def __str__(self):
        return self.name

