import json
from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from appliances.tests.factory import create_appliance
from sensors.tests.factory import create_sensor
from users.tests.factory import create_regular_dyeus_user

from sensors.models import Sensor

fake = Faker()


class TestUnauthenticatedSensorsViews(APITestCase):
    user = None
    appliance = None
    sensor = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)
        self.sensor = create_sensor(self.appliance)

    def test_cant_see_sensors(self):
        url = reverse('sensor-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_create_sensor(self):
        url = reverse('sensor-list')
        data = {
            'name': fake.sha256(),
            'code': fake.slug(),
            'appliance': self.appliance.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        sensors = Sensor.objects.filter(name=data['name'])
        self.assertEqual(sensors.count(), 0)

    def test_cant_see_sensor_detail(self):
        url = reverse('sensor-detail', args=(self.sensor.pk,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_change_sensor_detail(self):
        url = reverse('sensor-detail', args=(self.sensor.pk,))
        data = {
            'name': fake.sha256(),
            'code': fake.slug(),
            'appliance': self.appliance.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_see_recent(self):
        url = reverse('sensor-recent', args=(self.sensor.pk,))

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedSensorsViews(APITestCase):
    user1 = None
    user2 = None
    appliance = None
    appliance2 = None
    appliance3 = None
    sensor = None
    sensor2 = None
    sensor3 = None

    def setUp(self):
        self.user1 = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user1)
        self.sensor = create_sensor(self.appliance)
        self.appliance2 = create_appliance(self.user1)
        self.appliance2.is_active = True
        self.appliance2.save()
        self.sensor2 = create_sensor(self.appliance2)

        self.user2 = create_regular_dyeus_user()
        self.appliance3 = create_appliance(self.user2)
        self.sensor3 = create_sensor(self.appliance3)

        (token, _) = Token.objects.get_or_create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_can_see_only_own_sensors(self):
        url = reverse('sensor-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [
            {
                'id': s.id,
                'name': s.name,
                'code': s.code,
                'appliance': s.appliance.id
            } for s in [self.sensor, self.sensor2]
            ])

    def test_can_create_sensor(self):
        url = reverse('sensor-list')
        data = {
            'name': fake.name(),
            'code': fake.slug(),
            'appliance': self.appliance.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        sensors = Sensor.objects.filter(name=data['name'],
                                        appliance=self.appliance)
        self.assertEqual(sensors.count(), 1)

    def test_can_change_sensor(self):
        sid = self.sensor.id
        url = reverse('sensor-detail', args=(sid,))
        data = {
            'name': fake.name(),
            'code': fake.slug(),
            'appliance': self.appliance.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sensors = Sensor.objects.filter(id=sid)
        self.assertEqual(sensors.count(), 1)

        s = sensors.first()
        self.assertEqual(s.name, data['name'])
        self.assertEqual(s.code, data['code'])
        self.assertEqual(s.appliance.id, data['appliance'])

    def test_can_delete_sensor(self):
        sid = self.sensor.id
        url = reverse('sensor-detail', args=(sid,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        sensors = Sensor.objects.filter(id=sid)
        self.assertEqual(sensors.count(), 0)

    def test_can_see_recent(self):
        url = reverse('sensor-recent', args=(self.sensor.pk,))

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_create_sensor_of_active_appliance(self):
        url = reverse('sensor-list')
        data = {
            'name': fake.name(),
            'code': fake.slug(),
            'appliance': self.appliance2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        sensors = Sensor.objects.filter(name=data['name'],
                                        appliance=self.appliance)
        self.assertEqual(sensors.count(), 0)

    def test_cant_change_sensor_of_active_appliance(self):
        sid = self.sensor2.id
        url = reverse('sensor-detail', args=(sid,))
        data = {
            'name': fake.name(),
            'code': fake.slug(),
            'appliance': self.appliance.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_delete_sensor_of_active_appliance(self):
        sid = self.sensor2.id
        url = reverse('sensor-detail', args=(sid,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        sensors = Sensor.objects.filter(id=sid)
        self.assertEqual(sensors.count(), 1)

    def test_cant_create_sensor_to_other_user_appliance(self):
        url = reverse('sensor-list')
        data = {
            'name': fake.name(),
            'code': fake.slug(),
            'appliance': self.appliance3.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        sensors = Sensor.objects.filter(name=data['name'],
                                        appliance=self.appliance3)
        self.assertEqual(sensors.count(), 0)

    def test_cant_see_other_user_sensor(self):
        sid = self.sensor3.id
        url = reverse('sensor-detail', args=(sid,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_change_other_user_sensor(self):
        sid = self.sensor3.id
        url = reverse('sensor-detail', args=(sid,))
        data = {
            'name': fake.name(),
            'code': fake.slug(),
            'appliance': self.appliance.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_delete_other_user_sensor(self):
        sid = self.sensor3.id
        url = reverse('sensor-detail', args=(sid,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        sensors = Sensor.objects.filter(id=sid)
        self.assertEqual(sensors.count(), 1)

    def test_cant_see_recent_of_other_user_sensor(self):
        url = reverse('sensor-recent', args=(self.sensor3.pk,))

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
