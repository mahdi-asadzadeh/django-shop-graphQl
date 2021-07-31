from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Profile(models.Model):
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default='myimage/default_avatar.webp')
    age = models.PositiveIntegerField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')