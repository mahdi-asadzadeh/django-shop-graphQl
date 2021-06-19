from django.contrib.auth import get_user_model
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from .cart import Cart


User = get_user_model()


class CartType(DjangoObjectType):
	class Meta:
		model = User

	carts = GenericScalar()

	def resolve_carts(self, info):
		total_price = 0
		items = Cart.carts(self.id)
		for item in items:
			total_price += float(item['product_price'])
			
		return {
			'items': items,
			'total_price': total_price
		}
