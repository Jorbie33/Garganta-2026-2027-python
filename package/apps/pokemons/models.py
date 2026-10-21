from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    middle_name = models.CharField(max_length=50, unique=0)
    avatar = models.ImageField(upload_to='pokemons/avatars', default='pokemons/avatars/default.jpg')
    background = models.ImageField(upload_to='pokemons/background/', default='pokemons/background/bg default.png')

    def __str__(self):
        return self.username