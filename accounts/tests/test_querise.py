from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase


class AccountQueriseTest(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@gmail.com'
            )
        self.client.authenticate(self.user)
    
    def test_query_account(self):
        query = '''
            query {
                account {
                    id
                    username
                    email
                }
            }
        '''
        response = self.client.execute(query)
        data = response.data['account']
        self.assertEqual(self.user.username, data['username'])
        self.assertEqual(str(self.user.id), data['id'])
        self.assertEqual(self.user.email, data['email'])
        