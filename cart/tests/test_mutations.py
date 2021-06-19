from product.models import Product, Category
from cart.models import Cart, CartItem

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.conf import settings

from graphql_jwt.testcases import JSONWebTokenTestCase


class CartMutationsTest(JSONWebTokenTestCase):

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
        self.product = Product.objects.create(
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
        self.client.authenticate(user)

    def test_mutation_cart_add(self):
        query = '''
            mutation addToCart($productId: ID!, $quantity: Int!) {
                addToCart(productId: $productId, quantity: $quantity) {
                    response
                }
            }
        '''
        variables = {
          'productId': self.product.id,
          'quantity': 2
        }
        response = self.client.execute(query, variables)
        data = response.data
        self.assertEqual(data['addToCart']['response']['status'], 'success')

    def test_mutation_cart_clear(self):
        query = '''
            mutation cleareCart {
                cleareCart {
                    response
                }
            }
        '''
        response = self.client.execute(query)
        data = response.data
        self.assertEqual(data['cleareCart']['response']['status'], 'success')

    def test_mutation_cart_item_delete(self):
        query = '''
            mutation deleteCartitem($row_id: String!) {
                deleteCartitem(rowId: $row_id){
                    response
                }
            }
        '''
        variables = {
          'row_id': 'row id test', # row id not important
        }
        response = self.client.execute(query, variables)
        data = response.data
        self.assertEqual(data['deleteCartitem']['response']['status'], 'success')
        