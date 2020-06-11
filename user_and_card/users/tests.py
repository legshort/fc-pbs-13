from django.contrib.auth.models import User
from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = baker.make('auth.User', _quantity=3)

    def test_list(self):
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/users')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for user_response, user in zip(response.data['results'], self.users[::-1]):
            user_response = Munch(user_response)

            self.assertTrue(user_response.id)
            self.assertEqual(user_response.username, user.username)

    def test_create(self):
        data = {'username': 'abc'}
        response = self.client.post('/api/users', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])

    def test_detail(self):
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/users/{user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, user.username)

    def test_update(self):
        user = self.users[0]
        prev_username = user.username
        self.client.force_authenticate(user=user)
        data = {'username': 'new'}
        response = self.client.put(f'/api/users/{user.id}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)

        self.assertNotEqual(user_response.username, prev_username)
        self.assertEqual(user_response.username, data['username'])

    def test_delete(self):
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/{user.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(User.objects.filter(id=user.id).exists())
