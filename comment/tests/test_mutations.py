from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.conf import settings

from graphql_jwt.testcases import JSONWebTokenTestCase

from comment.models import Comment
from product.models import Product
from category.models import Category
from blog.models import Article


class CommentMutationsTest(JSONWebTokenTestCase):
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
		content_type = ContentType.objects.get_for_model(Product)
		self.comment = Comment.objects.create(
			content_type=content_type,
			object_id=self.product.id,
			rate=5,
			user=user,
			body='test body'
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
			tags='tag-article'
		)
		self.client.authenticate(user)

	def test_comment_delete(self):
		query = '''
			mutation deleteComment($id: ID!) {
				deleteComment(id: $id) {
					response
				}
			}
		'''
		variables = {
		  'id': self.comment.id,
		}

		response = self.client.execute(query, variables)
		data = response.data['deleteComment']
		self.assertEqual(data['response']['status'], 'success')
		self.assertEqual(Comment.objects.count(), 0)

	def test_comment_update(self):
		query = '''
			mutation updateComment($commentId: ID!, $body: String!, $rate: Int!) {
				updateComment(commentId: $commentId, body: $body, rate: $rate) {
					response
				}
			}
		'''
		variables = {
		  'commentId': self.comment.id,
		  'body': 'change body',
		  'rate': 1
		}
		response = self.client.execute(query, variables)
		data = response.data['updateComment']
		self.assertEqual(data['response']['status'], 'success')

	def test_comment_product_create(self):
		query = '''
			mutation createComment($typename: String!, $objectId: ID!, $rate: Int!, $body: String!) {
				createComment(typename: $typename, input: {
						objectId: $objectId,
						rate: $rate,
						body: $body,
					}){
						response
					}
			}
		'''
		variables = {
		  	'typename': 'ProductType',
			'objectId': self.product.id,
			'rate': 5,
			'body': 'body test.'
		}
		response = self.client.execute(query, variables)
		data = response.data['createComment']
		self.assertEqual(data['response']['status'], 'success')
		self.assertEqual(Comment.objects.get(id=2).body, 'body test.')
		self.assertEqual(Comment.objects.get(id=2).object_id, 1)
		self.assertEqual(Comment.objects.get(id=2).rate, '5')

	def test_comment_article_create(self):
		query = '''
			mutation createComment($typename: String!, $objectId: ID!, $rate: Int!, $body: String!) {
				createComment(typename: $typename, input: {
						objectId: $objectId,
						rate: $rate,
						body: $body,
					}){
						response
					}
			}
		'''
		variables = {
		  	'typename': 'ArticleType',
			'objectId': self.article.id,
			'rate': 5,
			'body': 'body test.'
		}
		response = self.client.execute(query, variables)
		data = response.data['createComment']
		self.assertEqual(data['response']['status'], 'success')
		self.assertEqual(Comment.objects.get(id=2).body, 'body test.')
		self.assertEqual(Comment.objects.get(id=2).object_id, 1)
		self.assertEqual(Comment.objects.get(id=2).rate, '5')
