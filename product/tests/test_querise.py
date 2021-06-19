import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from graphene_django.utils.testing import GraphQLTestCase
from product.models import Product
from category.models import Category


class ProductQueryTest(GraphQLTestCase):
	def setUp(self):
		image = SimpleUploadedFile(
			name='article_image.jpg', 
			content=open(f'{settings.STATIC_ROOT}/test/product_test.jpeg', 'rb').read(), 
			content_type='image/jpeg'
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

	def test_product_list(self):
		response = self.query(
			'''
				query {
					products {
						id
						title
						visit
						image
					}
				}
			'''
		)
		content = json.loads(response.content)
		data = content['data']
		self.assertEqual(data['products'][0]['id'], '1')
		self.assertEqual(data['products'][0]['title'], 'product')
		self.assertNotEqual(data['products'][0]['visit'], None)
		self.assertNotEqual(data['products'][0]['image'], None)
		self.assertResponseNoErrors(response)
	
	def test_product_detail(self):
		response = self.query(
			'''
				query productDetail($id: ID!, $slug: String!) {
					productDetail(id: $id, slug: $slug) {
						id
						title
						visit
						image
					}
				}
			''',
			variables={'id': self.product.id, 'slug': self.product.slug}
		)
		content = json.loads(response.content)
		data = content['data']
		self.assertEqual(data['productDetail']['id'], '1')
		self.assertEqual(data['productDetail']['title'], 'product')
		self.assertNotEqual(data['productDetail']['image'], None)
		self.assertResponseNoErrors(response)
