from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay, String
import graphene
from .models import GalleryProduct, Stone, Size, Color, Product
from taggit.models import Tag
from extensions.calculations import calculating_gold_jewelry
from comment.models import Comment
from comment.types import CommentType
from blog.types import ArticleType


class SimilarProductType(DjangoObjectType):

	class Meta:
		model = Product
		fields = '__all__'

	price = graphene.String()


class SimilarObjectsUnion(graphene.types.Union):
	class Meta:
		types = (SimilarProductType, ArticleType)


class ProductType(DjangoObjectType):

	class Meta:
		model = Product
		fields = '__all__'
	
	visit = graphene.Int()
	price = graphene.String()
	comments = graphene.List(CommentType)
	similar_objects = graphene.List(SimilarObjectsUnion)

	def resolve_visit(self, info):
		return self.visit
		
	def resolve_price(self, info):
		return calculating_gold_jewelry(self)
	
	def resolve_comments(self, info):
		return Comment.objects.filter_by_instance(instance=self)
	
	def resolve_similar_objects(self, info):
		return self.tags.similar_objects()[:15]
		 

class StoneType(DjangoObjectType):
	class Meta:
		model = Stone


class ProductGalleryType(DjangoObjectType):
	class Meta:
		model = GalleryProduct


class SizeType(DjangoObjectType):
	class Meta:
		model = Size


class ColorType(DjangoObjectType):
	class Meta:
		model = Color
