from product.types import ProductType, Product
from blog.types import ArticleType, Article
import graphene
from django.db.models import Q
from itertools import chain


class SearchUnion(graphene.types.Union):
	class Meta:
		types = (ProductType, ArticleType)


class SearchQuery(graphene.ObjectType):
	search_all_app = graphene.List(SearchUnion, search=graphene.String())
	
	def resolve_search_all_app(self, info, search):
		if search:
			product_filter = (
				Q(title__icontains=search)|
				Q(slug__icontains=search)|
				Q(category__name__icontains=search)|
				Q(category__slug__icontains=search)|
				Q(body__icontains=search)|
				Q(tags__name__icontains=search)
			)
			article_filter = (
				Q(name__icontains=search)|
				Q(slug__icontains=search)|
				Q(body__icontains=search)|
				Q(tags__name__icontains=search)
			)
			product_query = Product.objects.filter(product_filter).distinct()
			article_query = Article.objects.filter(article_filter).distinct()
		
		return list(chain(product_query, article_query))
