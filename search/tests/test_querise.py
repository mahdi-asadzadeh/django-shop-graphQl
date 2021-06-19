import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from graphene_django.utils.testing import GraphQLTestCase
from product.models import Product
from blog.models import Article
from category.models import Category


class SearchQueryTest(GraphQLTestCase):
	def setUp(self):
		image = SimpleUploadedFile(
			name='article_image.jpg', 
			content=open(f'{settings.STATIC_ROOT}/test/product_test.jpeg', 'rb').read(), 
			content_type='image/jpeg'
		)
		category = Category.objects.create(name='category', slug='slug')
		self.product = Product.objects.create(
			title='product test',
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
		image = SimpleUploadedFile(
			name='article_image.jpg', 
			content=open(f'{settings.STATIC_ROOT}/test/article_image.jpg', 'rb').read(), 
			content_type='image/jpeg'
		)
		self.article = Article.objects.create(
			name='article test',
			slug='article-test',
			image=image,
			body='article body',
			status='p',
			tags='tag'
		)
		
	def test_query_search(self):
		response = self.query(
			'''
			query searchAllApp($search: String!) {
				searchAllApp(search: $search) {
					... on ProductType {
						__typename
						id
						title
						slug
					}
					... on ArticleType {
						__typename
						id
						name
						slug
					}
				}
			}
			''',
			variables={'search': 'test'}
		)
		content = json.loads(response.content)
		data = content['data']['searchAllApp']
		self.assertEqual(data[0]['__typename'], 'ProductType')
		self.assertEqual(data[1]['__typename'], 'ArticleType')
		self.assertResponseNoErrors(response)
