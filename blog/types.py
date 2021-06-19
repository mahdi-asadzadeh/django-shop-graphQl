import graphene

from graphene_django.types import DjangoObjectType
from .models import Article


class ArticleType(DjangoObjectType):
	class Meta:
		model = Article

	visit = graphene.Int()

	def resolve_visit(self, info):
		return self.visit