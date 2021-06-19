import graphene
from zeep import Client
from graphql_jwt.decorators import login_required
from graphene.types.generic import GenericScalar
from order.models import Order, OrderItem
from product.models import Product
from cart.cart import Cart


# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.


# class VerifyPayment(graphene.Mutation):
#     class Arguments:
#         status = graphene.String(required=True)
#         authority = graphene.String(required=True)
	
#     response = graphene.String(required=True)

#     def mutate(parent, info, status, authority):
#         if status == 'OK':
#             try:
#                 order = Order.objects.get(authority=authority)
#                 result = client.service.PaymentVerification(MERCHANT, authority, order.price)
#                 if result.Status == 100:
#                     order.paid = True
#                     order.save()
#                     return VerifyPayment(response=f'Transaction success.\nRefID: {str(result.RefID)}')
#                 elif result.Status == 101:
#                     return VerifyPayment(response=f'Transaction submitted : {str(result.Status)}')
#                 else:
#                     return VerifyPayment(response=f'Transaction failed.\nStatus: {str(result.Status)}')

#             except Order.DoesNotExist:
#                 raise Exception('Order matching query does not exist.')
#         else:
#             return VerifyPayment(response=f'Transaction failed or canceled by user .')


# class SendRequest(graphene.Mutation):
#     class Arguments:
#         order_id = graphene.ID()

#     redirect_url = graphene.String()

#     @login_required
#     def mutate(parent, info, order_id):
#         user = info.context.user
#         try:
#             order = Order.objects.get(id=order_id, user=user)
#             if order.paid != True:
#                 amount = order.price # Toman / Required
#                 result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
#                 if result.Status == 100:
#                     order.authority = result.Authority
#                     return SendRequest(redirect_url=f'https://www.zarinpal.com/pg/StartPay/{str(result.Authority)}')

#                 else:
#                     raise Exception(f'Error code: {str(result.Status)}')

#             else:
#                 raise Exception('Paid order .')

#         except Order.DoesNotExist:
#             raise Exception('order dose not exist .')


class CreateOrder(graphene.Mutation):
	class Arguments:
		address = graphene.String()
	
	response = GenericScalar()

	@login_required
	def mutate(parent, info, address): 
		user = info.context.user
  
		carts = Cart.carts(user.id)
		if carts == []:
			return CreateOrder(response={'status': 'error', 'message': 'carts are empty.'})
		total_price = 0
		for cart in carts:
			total_price += float(cart['product_price'])
		order = Order.objects.create(
			user=user,
			price=total_price,
			paid=False,
			address=address
			)
		for cart in carts:
		    OrderItem.objects.create(
		        product=Product.objects.get(id=cart['product_id']),
		        order=order,
		    )
		Cart.delete_all_carts(user.id)
		return CreateOrder(response={'status': 'success', 'message': 'create order.'})

		
class OrderMutations(graphene.ObjectType):
	create_order = CreateOrder.Field()
	# send_request = SendRequest.Field()
	# verify_payment = VerifyPayment.Field()
	