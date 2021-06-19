from django.core.cache import cache
from django.conf import settings
from django.db.models import Q

from blog.models import Article
from .types import ArticleType
import graphene

class ArticleQuery(graphene.ObjectType):

	articles = graphene.List(
		ArticleType, 
		search=graphene.String(), 
		first=graphene.Int(), 
		skip=graphene.Int(),
		order_visit=graphene.Boolean(),
		order_rating=graphene.Boolean()
		)
	article_detail = graphene.Field(ArticleType, id=graphene.ID(), slug=graphene.String())

	def resolve_articles(
		parent, 
		info, 
		search=None, 
		first=None, 
		skip=None,
		order_visit=None,
		order_rating=None,
		):
		query = None
		
		if 'articles' in cache:
			query = cache.get('articles')
			
		else:
			query = Article.objects.filter(status='p')
			cache.set('articles', query, timeout=settings.ARTICLES_TIMEOUT)
			
		if search:
			filter = (
				Q(name__icontains=search) |
				Q(slug__icontains=search) |
				Q(body__icontains=search) |
				Q(tags__name__icontains=search)
			)
			query = query.filter(filter).distinct()

		if skip:
			query = query[skip:]

		if first:
			query = query[:first]

		if order_visit != None:
			if order_visit:
				query = sorted(query, key=lambda t: -t.visit)
			else:
				query = sorted(query, key=lambda t: t.visit)

		if order_rating != None:
			if order_rating:
				query = sorted(query, key=lambda t: -t.rating)
			else:
				query = sorted(query, key=lambda t: t.rating)

		return query
	
	def resolve_article_detail(parent, info, id, slug):   
		query = Article.objects.get(id=id, status='p') 
		settings.REDIS.hsetnx('article_visit', query.id, 0)
		settings.REDIS.hincrby('article_visit', query.id)
		return query