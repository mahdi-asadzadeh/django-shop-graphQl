from graphene_django.types import DjangoObjectType
from .models import Comment


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
