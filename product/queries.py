
import graphene
from graphene import types
from graphene.relay import node
from graphene_django.types import ObjectType

from django.core.cache import cache
from django.conf import settings
from django.db.models import Q

from .types import ProductType
from .models import Product


class ProductQuery(ObjectType):

	products = graphene.List(
		ProductType, 
	    search=graphene.String(), 
		first=graphene.Int(), 
		skip=graphene.Int(),
		gold_or_jewelry=graphene.Boolean(),
		special_offer=graphene.Boolean(),
		order_sale_number=graphene.Boolean(),
		order_price=graphene.Boolean(),
		order_rating=graphene.Boolean(),
		)
	product_detail = graphene.Field(ProductType, id=graphene.ID(), slug=graphene.String())

	def resolve_products(
		parent, 
		info, 
		search=None, 
		first=None, 
		skip=None,
		gold_or_jewelry=None,
		special_offer=None,
		order_sale_number=None,
		order_price=None,
		order_rating=None
		):
		query = None
		
		if 'products' in cache:
			query = cache.get('products')
			
		else:
			query = Product.objects.filter(status='p')
			cache.set('products', query, timeout=settings.PRODUCTS_TIMEOUT)
			
		if search:
			filter = (
				Q(title__icontains=search) |
				Q(slug__icontains=search) |
				Q(body__icontains=search) |
				Q(tags__name__icontains=search)
			)
			query = query.filter(filter).distinct()

		if skip:
			query = query[skip:]

		if first:
			query = query[:first]
		
		if gold_or_jewelry != None:
			if gold_or_jewelry:
				query = query.filter(gold_or_jewelry=True)
			else:
				query = query.filter(gold_or_jewelry=False)

		if special_offer != None:
			if special_offer:
			 	query = query.filter(special_offer=True)
			else:
			 	query = query.filter(special_offer=False)

		if order_sale_number != None:
			if order_sale_number:
				query = sorted(query, key=lambda t: -t.sale_number)
			else:
				query = sorted(query, key=lambda t: t.sale_number)
		
		if order_price != None:
			if order_price:
				query = sorted(query, key=lambda t: -t.price)
			else:
				query = sorted(query, key=lambda t: t.price)

		if order_rating != None:
			if order_rating:
				query = sorted(query, key=lambda t: -t.rating)
			else:
				query = sorted(query, key=lambda t: t.rating)

		return query
	
	def resolve_product_detail(parent, info, id, slug):   
		query = Product.objects.get(id=id, status='p') 
		settings.REDIS.hsetnx('product_visit', query.id, 0)
		settings.REDIS.hincrby('product_visit', query.id)
		return query
