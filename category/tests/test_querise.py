import json

from graphene_django.utils.testing import GraphQLTestCase
from category.models import Category


class CategoryQueryTest(GraphQLTestCase):
    def setUp(self):
        Category.objects.create(name='category')

    def test_query_category_list(self):
            response = self.query(
                '''
                    query {
                        categories{
                            id
                            name
                        }
                    }
                '''
            )
            content = json.loads(response.content)
            data = content['data']
            self.assertEqual(data['categories'][0]['id'], '1')
            self.assertEqual(data['categories'][0]['name'], 'category')
            self.assertResponseNoErrors(response)
            
