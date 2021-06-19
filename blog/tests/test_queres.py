import json

from graphene_django.utils.testing import GraphQLTestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from blog.models import Article


class ArticleQueryTest(GraphQLTestCase):
	def setUp(self):
		image = SimpleUploadedFile(
			name='article_image.jpg', 
			content=open(f'{settings.STATIC_ROOT}/test/article_image.jpg', 'rb').read(), 
			content_type='image/jpeg'
		)

		self.article = Article.objects.create(
			name='article test',
			slug='article1',
			image=image,
			body='article body',
			status='p',
			tags='tag-article'
		)

	def test_query_articles_list(self):
		response = self.query(
			'''
				query {
					articles {
						id
						name
						visit
					}
				}
			'''
		)
		content = json.loads(response.content)
		self.assertResponseNoErrors(response)

	def test_query_article_detail(self):
		response = self.query(
			'''
			query articleDetail($id: ID!, $slug: String!) {
				articleDetail(id: $id, slug: $slug) {
					id
					name
					slug
				}
			}
			''',
			# Slug is not important, anything can be .
			variables={'id':self.article.id, 'slug': self.article.slug}
		)
		content = json.loads(response.content)
		data = content['data']['articleDetail']

		self.assertEqual(data['id'], '1')
		self.assertEqual(data['slug'], 'article1')
		self.assertResponseNoErrors(response)
		