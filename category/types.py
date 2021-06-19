from django.db import models
import graphene
from graphene_django.types import DjangoObjectType
from .models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        