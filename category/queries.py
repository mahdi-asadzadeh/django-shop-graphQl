from django.core.cache import cache
from django.conf import settings

import graphene
from .types import CategoryType
from .models import Category 


class CategoryQuery(graphene.ObjectType):
	categories = graphene.List(CategoryType)

	def resolve_categories(parent, info):
		query = None
		if 'gategories' in cache:
			query = cache.get('gategories')
			
		else:
			gategories = Category.objects.filter(parent=None)
			cache.set('gategories', gategories, timeout=settings.CATEGORIES_TIMEOUT)
			query = gategories

		return query
