from cart.models import Cart
from django.contrib.auth import get_user_model

from graphql_jwt.testcases import JSONWebTokenTestCase


class CartQueryTest(JSONWebTokenTestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@gmail.com'
            )
        self.client.authenticate(user)

    def test_query_cart_list(self):
        query = '''
            query carts {
                carts {
                    carts
                }
            }
        '''

        response = self.client.execute(query)
        data = response.data['carts']
        self.assertEqual(data['carts']['total_price'], 0)
        self.assertEqual(data['carts']['items'], [])
 
