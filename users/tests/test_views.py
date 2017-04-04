import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.tests.factory import create_regular_dyeus_user


class TestUnauthenticatedUsersViews(APITestCase):
    user = None

    def setUp(self):
        self.user = create_regular_dyeus_user()

    def test_fails_auth_test(self):
        url = reverse('auth-test')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_get_user_data(self):
        url = reverse('user-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedUsersViews(APITestCase):
    user = None

    def setUp(self):
        self.user = create_regular_dyeus_user()

        (token, _) = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_passes_auth_test(self):
        url = reverse('auth-test')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_user_data(self):
        url = reverse('user-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
            'username': self.user.username
            })
