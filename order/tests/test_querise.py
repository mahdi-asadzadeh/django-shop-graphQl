from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.conf import settings

from graphql_jwt.testcases import JSONWebTokenTestCase

from product.models import Product, Category
from cart.models import Cart, CartItem
from order.models import Order, OrderItem


class OrderQueryTest(JSONWebTokenTestCase):
    def setUp(self):
        image = SimpleUploadedFile(
			name='article_image.jpg', 
			content=open(f'{settings.STATIC_ROOT}/test/product_test.jpeg', 'rb').read(), 
			content_type='image/jpeg'
		)
        user = get_user_model().objects.create_user(
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
        self.cart = Cart.objects.create(user=user)
        CartItem.objects.create(
            cart=self.cart, 
            product=product,
            quantity=2
            )
        order = Order.objects.create(
            user=user,
            price=self.cart.get_total_price,
            paid=False,
        )
        OrderItem.objects.create(
            product=product,
            order=order
        )
        self.client.authenticate(user)
    
    def test_query_order_list(self):
        query = '''
            query orders {
                orders {
                    id
                    price
                    paid
                    items {
                        id
                        product {
                            id
                            title
                        }
                    }
                }
            }
        '''
        response = self.client.execute(query)
        data = response.data['orders']
        self.assertEqual(data[0]['paid'], False)
        self.assertEqual(data[0]['price'], '1068.26')
        self.assertEqual(data[0]['items'][0]['product']['id'], '1')
        self.assertEqual(data[0]['items'][0]['product']['title'], 'product')
        