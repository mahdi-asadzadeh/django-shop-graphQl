
import graphene
from decimal import Decimal
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required
from product.models import Product
from .cart import Cart


class AddToCart(graphene.Mutation):
	class Arguments:
		product_id = graphene.ID(required=True)
		quantity = graphene.Int(required=True)
	
	response = GenericScalar()

	@login_required
	def mutate(parent, info, product_id, quantity=1):
		user = info.context.user
		try:
			product = Product.objects.get(id=product_id)
			Cart.add_to_cart(
				user_id = user.id,
				product_id = product.id,
				product_image = str(product.image.url),
				product_price = str(Decimal(product.price) * quantity),
				product_quantity = quantity,
			)
			return AddToCart(response={'status': 'success', 'message': 'add to cart.'})

		except Product.DoesNotExist:
			return AddToCart(response={'status': 'error', 'message': 'Product matching query does not exist.'})


class DeleteCartItem(graphene.Mutation):
	class Arguments:
		row_id = graphene.String(required=True)
	
	response = GenericScalar()

	@login_required
	def mutate(parent, info, row_id):
		user = info.context.user
		Cart.delete_cart(user.id, row_id)
		return DeleteCartItem(response={'status': 'success', 'message': 'delete cart.'})


class CleareCartItem(graphene.Mutation):

	response = GenericScalar()

	@login_required
	def mutate(parent, info):
		user = info.context.user
		Cart.delete_all_carts(user.id)
		return CleareCartItem(response={'status': 'success', 'message': 'cleare cart.'})


class CartMutation(graphene.ObjectType):
	add_to_cart = AddToCart.Field()
	delete_cartitem = DeleteCartItem.Field()
	cleare_cart = CleareCartItem.Field()
	
































































# import graphene
# from .models import Cart, CartItem
# from product.models import Product
# from graphql_jwt.decorators import login_required


# class AddToCart(graphene.Mutation):
# 	class Arguments:
# 		product_id = graphene.ID(required=True)
# 		quantity = graphene.Int(required=True)
# 		update_quantity = graphene.Boolean(default_value=False)
	
# 	ok = graphene.Boolean(default_value=False)

# 	@login_required
# 	def mutate(parent, info, product_id, update_quantity, quantity=1):
# 		user = info.context.user
# 		try:
# 			cart = user.cart
# 		except Cart.DoesNotExist:
# 			cart = Cart.objects.create(user=user)
		
# 		try:
# 			product = Product.objects.get(id=product_id)
# 		except Product.DoesNotExist:
# 			raise Exception('Product does not exist')

# 		products = []
# 		for item in cart.items.all():
# 			products.append(item.product)

# 		if product not in products:
# 			CartItem.objects.create(
# 				cart=cart,
# 				product=product,
# 				quantity=quantity,
# 			)
# 		cart_item = CartItem.objects.get(cart=cart, product=product)
# 		if update_quantity:
# 			cart_item.quantity = quantity
# 		else:
# 			cart_item.quantity += int(quantity)
# 		cart_item.save()

# 		return AddToCart(ok=True)
	

# class DeleteCartItem(graphene.Mutation):
# 	class Arguments:
# 		cart_item_id = graphene.ID(required=True)
	
# 	ok = graphene.Boolean(default_value=False)

# 	@login_required
# 	def mutate(parent, info, cart_item_id):
# 		user = info.context.user
# 		try:
# 			cart = user.cart
# 		except Cart.DoesNotExist:
# 			cart = Cart.objects.create(user=user)

# 		try:
# 			CartItem.objects.get(id=cart_item_id, cart=cart).delete()
# 		except CartItem.DoesNotExist:
# 			raise Exception('Cart item does not exist')
		
# 		return DeleteCartItem(ok=True)


# class CleareCartItem(graphene.Mutation):
# 	ok = graphene.Boolean(default_value=False)

# 	@login_required
# 	def mutate(parent, info):
# 		user = info.context.user
# 		try:
# 			cart = user.cart
# 		except Cart.DoesNotExist:
# 			cart = Cart.objects.create(user=user)

# 		cart.items.all().delete()                
# 		return CleareCartItem(ok=True)


# class CartMutation(graphene.ObjectType):
# 	add_to_cart = AddToCart.Field()
# 	delete_cartitem = DeleteCartItem.Field()
# 	cleare_cart = CleareCartItem.Field()
	