from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.conf import settings

from cart.models import Cart, CartItem
from product.models import Product, Category

from graphql_jwt.testcases import JSONWebTokenTestCase


class OrderMutationsTest(JSONWebTokenTestCase):
    def setUp(self):
        image = SimpleUploadedFile(
			name='article_image.jpg', 
			content=open(f'{settings.STATIC_ROOT}/test/product_test.jpeg', 'rb').read(), 
			content_type='image/jpeg'
		)
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@gmail.com'
            )
        category = Category.objects.create(name='category', slug='slug')
        product = Product.objects.create(
            title='product',
            slug='product',
            carat='8',
            weight=1,
            length=1,
            width=1,
            category=category,
            site_rate=0.2,
            gold_or_jewelry=True,
            is_rate_fixed=True,
            provider_gold_rate=0.8,
            body='body',
            status='p',
            image=image,
            tags='tag'
        )
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=self.cart, 
            product=product,
            quantity=2
            )
        self.client.authenticate(self.user)
    
    def test_order_create(self):
        query = '''
            mutation createOrder {
                createOrder {
                    response
                }
            }
        '''
        variables = {
          'cartId': self.cart.id,
        }
        response = self.client.execute(query, variables)
        data = response.data['createOrder']

        self.assertEqual(data['response']['status'], 'error')
        self.assertEqual(data['response']['message'], 'carts are empty.')
        self.assertEqual(self.user.orders.count(), 0)
