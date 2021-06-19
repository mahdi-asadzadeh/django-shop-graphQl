import json
from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase
from graphene_django.utils.testing import GraphQLTestCase


class AccountMutationsTest(JSONWebTokenTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test',
            email='test@gmail.com'
            )
        self.client.authenticate(self.user)
    
    def test_mutation_change_email(self):
        query = '''
            mutation changeEmail($email: String!) {
                changeEmail(email: $email) {
                    response
                }
            }
        '''
        variables = {
            'email': 'email_change@gmail.com',
        }
        response = self.client.execute(query, variables)
        data = response.data['changeEmail']
        self.assertEqual(data['response']['status'], 'success')
        self.assertEqual(get_user_model().objects.get(email='email_change@gmail.com').is_active, False)

    def test_mutation_reset_password(self):
        query = '''
            mutation resetPassword($email: String!) {
                resetPassword(email: $email) {
                    response
                }
            }
        '''
        variables = {
            'email': self.user.email,
        }
        response = self.client.execute(query, variables)
        data = response.data['resetPassword']
        self.assertEqual(data['response']['status'], 'success')
    
    def test_mutation_change_password(self):
        query = '''
            mutation changePassword($newPassword: String!, $oldPassword: String!) {
                changePassword(newPassword: $newPassword, oldPassword: $oldPassword) {
                    response
                }
            }
        '''
        variables = {
            'newPassword': 'new_password',
            'oldPassword': 'test',
        }
        response = self.client.execute(query, variables)
        data = response.data['changePassword']
        self.assertEqual(data['response']['status'], 'success')

    def test_mutation_create_account(self):
        query = '''
            mutation createAccount($username: String!, $email: String!, $password: String!, $first_name: String!, $last_name: String!) {
                createAccount(input: {
                    username: $username
                    email: $email
                    password: $password
                    firstName: $first_name
                    lastName: $last_name
                }) {
                    response
                }
            }
        '''
        variables={
            'username': 'create_user',
            'email': 'create_user@gmail.com',
            'password': 'create_user_password',
            'first_name': 'create user',
            'last_name': 'create user'
        }

        response = self.client.execute(query, variables)
        data = response.data['createAccount']
        self.assertEqual(data['response']['status'], 'success')
        self.assertEqual(get_user_model().objects.get(email='create_user@gmail.com').username, 'create_user')
        self.assertEqual(get_user_model().objects.get(email='create_user@gmail.com').first_name, 'create user')

    def test_mutation_updata_account(self):
        query = ''' 
            mutation updateAccount($first_name: String!, $last_name: String!, $username: String!) {
                    updateAccount(
                        firstName: $first_name
                        lastName: $last_name
                        username: $username
                    ) {
                        response
                    }
                }
        '''
        variables = {
            'first_name': 'updata account',
            'last_name': 'updata',
            'username': 'updata',
        }
        response = self.client.execute(query, variables)
        data = response.data['updateAccount']
        self.assertEqual(data['response']['status'], 'success')
        self.assertEqual(get_user_model().objects.get(email='test@gmail.com').first_name, 'updata account')
        self.assertEqual(get_user_model().objects.get(email='test@gmail.com').last_name, 'updata')
        self.assertEqual(get_user_model().objects.get(email='test@gmail.com').username, 'updata')

    def test_mutation_updata_profile(self):
        query = ''' 
            mutation updateProfile($age: Int!, $bio: String!) {
                    updateProfile(
                        age: $age
                        bio: $bio
                    ) {
                        response
                    }
                }
        '''
        variables = {
            'age': 5,
            'bio': 'bio updata',

        }
        response = self.client.execute(query, variables)
        data = response.data['updateProfile']
        self.assertEqual(data['response']['status'], 'success')
        self.assertEqual(get_user_model().objects.get(email='test@gmail.com').profile.bio, 'bio updata')
        self.assertEqual(get_user_model().objects.get(email='test@gmail.com').profile.age, 5)
