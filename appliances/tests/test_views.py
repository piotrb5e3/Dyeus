import json
from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from appliances.tests.factory import create_appliance
from sensors.tests.factory import create_sensor
from users.tests.factory import create_regular_dyeus_user

from appliances.models import Appliance

fake = Faker()


class TestUnauthenticatedAppliancesViews(APITestCase):
    user1 = None
    user2 = None
    appliance1 = None
    appliance2 = None
    appliance3 = None
    sensor1 = None
    sensor2 = None
    sensor3 = None

    def setUp(self):
        self.user1 = create_regular_dyeus_user()
        self.appliance1 = create_appliance(self.user1)
        self.sensor1 = create_sensor(self.appliance1)
        self.sensor2 = create_sensor(self.appliance1)
        self.appliance2 = create_appliance(self.user1)

        self.user2 = create_regular_dyeus_user()
        self.appliance3 = create_appliance(self.user2)
        self.sensor3 = create_sensor(self.appliance3)

    def test_cant_see_appliances(self):
        url = reverse('appliance-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_create_appliance(self):
        url = reverse('appliance-list')
        data = {
            'name': fake.sha256(),
            'authenticationModel': 'token',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        appliances = Appliance.objects.filter(name=data['name'])
        self.assertEqual(appliances.count(), 0)

    def test_cant_see_appliance_detail(self):
        url = reverse('appliance-detail', args=(self.appliance1.pk,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_change_appliance_detail(self):
        url = reverse('appliance-detail', args=(self.appliance1.pk,))
        data = {
            'name': fake.sha256(),
            'authenticationModel': 'token',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_deactivate_appliance(self):
        url = reverse('appliance-deactivate', args=(self.appliance1.pk,))

        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_activate_appliance(self):
        url = reverse('appliance-activate', args=(self.appliance1.pk,))

        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedApplianceViews(APITestCase):
    user1 = None
    user2 = None
    appliance1 = None
    appliance2 = None
    appliance3 = None
    appliance4 = None
    sensor1 = None
    sensor2 = None
    sensor3 = None

    def setUp(self):
        self.user1 = create_regular_dyeus_user()
        self.appliance1 = create_appliance(self.user1)
        self.sensor1 = create_sensor(self.appliance1)
        self.sensor2 = create_sensor(self.appliance1)
        self.appliance2 = create_appliance(self.user1)
        self.appliance2.is_active = True
        self.appliance2.save()

        self.user2 = create_regular_dyeus_user()
        self.appliance3 = create_appliance(self.user2)
        self.sensor3 = create_sensor(self.appliance3)
        self.appliance4 = create_appliance(self.user2)
        self.appliance4.is_active = True
        self.appliance4.save()

        (token, _) = Token.objects.get_or_create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_can_see_only_own_appliances(self):
        url = reverse('appliance-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [
            {
                'id': a.id,
                'name': a.name,
                'sensors': [
                    {
                        'id': s.id,
                        'name': s.name,
                        'code': s.code,
                        'appliance': s.appliance.id
                    } for s in a.sensors.all()],
                'is_active': a.is_active,
                'authentication_model': a.authentication_model,
                'authentication_value': a.authentication_value,

            } for a in [self.appliance1, self.appliance2]])

    def test_can_create_appliance(self):
        url = reverse('appliance-list')
        data = {
            'name': fake.name(),
            'authentication_model': 'token',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        appliances = Appliance.objects.filter(name=data['name'],
                                              owner=self.user1)
        self.assertEqual(appliances.count(), 1)

    def test_can_create_appliance_with_gcm(self):
        url = reverse('appliance-list')
        data = {
            'name': fake.name(),
            'authentication_model': 'gcm_aes',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        appliances = Appliance.objects.filter(name=data['name'],
                                              owner=self.user1)
        self.assertEqual(appliances.count(), 1)
        a = appliances.first()
        self.assertEqual(len(a.authentication_value), 32)

    def test_can_change_appliance(self):
        url = reverse('appliance-detail', args=(self.appliance1.id,))
        data = {
            'name': fake.name(),
            'authentication_model': 'token',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        appliances = Appliance.objects.filter(id=self.appliance1.id,
                                              name=data['name'],
                                              owner=self.user1)
        self.assertEqual(appliances.count(), 1)

    def test_cant_see_other_user_appliance_detail(self):
        url = reverse('appliance-detail', args=(self.appliance3.id,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_change_other_user_appliance(self):
        url = reverse('appliance-detail', args=(self.appliance3.id,))
        data = {
            'name': fake.name(),
            'authentication_model': 'token',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        appliances = Appliance.objects.filter(id=self.appliance3.id,
                                              name=data['name'])
        self.assertEqual(appliances.count(), 0)

    def test_can_delete_appliance(self):
        url = reverse('appliance-detail', args=(self.appliance2.id,))
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        appliances = Appliance.objects.filter(id=self.appliance2.id)
        self.assertEqual(appliances.count(), 0)

    def test_cant_delete_other_user_appliance(self):
        url = reverse('appliance-detail', args=(self.appliance3.id,))
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        appliances = Appliance.objects.filter(id=self.appliance3.id)
        self.assertEqual(appliances.count(), 1)

    def test_can_activate_appliance(self):
        aid = self.appliance1.id
        url = reverse('appliance-activate', args=(aid,))
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, False)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, True)

    def test_can_deactivate_appliance(self):
        aid = self.appliance2.id
        url = reverse('appliance-deactivate', args=(aid,))
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, True)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, False)

    def test_cant_activate_active_appliance(self):
        aid = self.appliance2.id
        url = reverse('appliance-activate', args=(aid,))
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, True)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, True)

    def test_cant_deactivate_inactive_appliance(self):
        aid = self.appliance1.id
        url = reverse('appliance-deactivate', args=(aid,))
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, False)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, False)

    def test_cant_activate_other_user_appliance(self):
        aid = self.appliance3.id
        url = reverse('appliance-activate', args=(aid,))
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, False)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, False)

    def test_cant_deactivate_other_user_appliance(self):
        aid = self.appliance4.id
        url = reverse('appliance-deactivate', args=(aid,))
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, True)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Appliance.objects.get(pk=aid).is_active, True)
