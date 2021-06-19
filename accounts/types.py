from django.db import models
from graphene_django.types import DjangoObjectType
from .models import User, Profile


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ['password']
