import base64

from datetime import datetime, timezone, timedelta
from random import random
from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend

from appliances.tests.factory import (create_appliance,
                                      create_sha_authenticated_appliance, )
from sensors.tests.factory import create_sensor
from users.tests.factory import create_regular_dyeus_user

from appliances.models import Reading

from sensors.models import SensorValue

fake = Faker()


class TestTokenCollectViews(APITestCase):
    user = None
    appliance = None
    sensor = None
    sensor2 = None
    sensor3 = None
    appliance2 = None
    sensor4 = None
    url = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)
        self.appliance.is_active = True
        self.appliance.save()
        self.sensor = create_sensor(self.appliance)
        self.sensor2 = create_sensor(self.appliance)
        self.sensor3 = create_sensor(self.appliance)

        self.appliance2 = create_appliance(self.user)
        self.sensor4 = create_sensor(self.appliance2)
        self.url = reverse('collect-by-token')

    def test_cant_submit_empty_post(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_submit_without_correct_token(self):
        data = {
            'token': 'this_is_a_bad_token ',
            'sensors': {
                self.sensor.code: str(random()),
                self.sensor2.code: str(random()),
                self.sensor3.code: str(random()),
            },
            'timestamp': _recent_iso_timestamp()
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 0)

    def test_cant_submit_to_inactive_appliance(self):
        data = {
            'token': self.appliance2.authentication_value,
            'sensors': {
                self.sensor4.code: str(random()),
            },
            'timestamp': _recent_iso_timestamp()
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        readings = Reading.objects.filter(appliance=self.appliance2)
        self.assertEqual(readings.count(), 0)

    def test_cant_submit_without_all_sensor_readings(self):
        data = {
            'token': self.appliance.authentication_value,
            'sensors': {
                self.sensor.code: str(random()),
                self.sensor2.code: str(random()),
                'BaD-c0d3$$': str(random()),
            },
            'timestamp': _recent_iso_timestamp()
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 0)

    def test_can_submit_readings(self):
        data = {
            'id': self.appliance.id,
            'token': self.appliance.authentication_value,
            'sensors': {
                self.sensor.code: str(random()),
                self.sensor2.code: str(random()),
                self.sensor3.code: str(random()),
            },
            'timestamp': _recent_iso_timestamp()
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 1)
        reading = readings.first()

        delta = datetime.now(tz=timezone.utc) - reading.timestamp

        self.assertEqual(reading.appliance, self.appliance)
        self.assertLessEqual(delta, timedelta(days=60))

        sv = SensorValue.objects.filter(sensor=self.sensor)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.reading, reading)
        self.assertEqual(sv.value, data['sensors'][self.sensor.code])

        sv = SensorValue.objects.filter(sensor=self.sensor2)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.reading, reading)
        self.assertEqual(sv.value, data['sensors'][self.sensor2.code])

        sv = SensorValue.objects.filter(sensor=self.sensor3)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.reading, reading)
        self.assertEqual(sv.value, data['sensors'][self.sensor3.code])

    def test_cant_submit_readings_without_timestamp(self):
        data = {
            'id': self.appliance.id,
            'token': self.appliance.authentication_value,
            'sensors': {
                self.sensor.code: str(random()),
                self.sensor2.code: str(random()),
                self.sensor3.code: str(random()),
            }
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_submit_readings_with_bad_timestamp(self):
        data = {
            'id': self.appliance.id,
            'token': self.appliance.authentication_value,
            'sensors': {
                self.sensor.code: str(random()),
                self.sensor2.code: str(random()),
                self.sensor3.code: str(random()),
            },
            'timestamp': "BAD_TIMESTAMP"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_submit_readings_with_bad_timestamp2(self):
        data = {
            'id': self.appliance.id,
            'token': self.appliance.authentication_value,
            'sensors': {
                self.sensor.code: str(random()),
                self.sensor2.code: str(random()),
                self.sensor3.code: str(random()),
            },
            'timestamp': {
                'foo': 'bar',
            },
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_submit_readings_with_bad_timestamp3(self):
        data = {
            'id': self.appliance.id,
            'token': self.appliance.authentication_value,
            'sensors': {
                self.sensor.code: str(random()),
                self.sensor2.code: str(random()),
                self.sensor3.code: str(random()),
            },
            'timestamp': True
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestSHAHMACCollectViews(APITestCase):
    user = None
    appliance = None
    sensor = None
    sensor2 = None
    sensor3 = None
    appliance2 = None
    sensor4 = None
    url = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_sha_authenticated_appliance(self.user)
        self.appliance.is_active = True
        self.appliance.save()
        self.sensor = create_sensor(self.appliance)
        self.sensor2 = create_sensor(self.appliance)
        self.sensor3 = create_sensor(self.appliance)

        self.appliance2 = create_appliance(self.user)
        self.sensor4 = create_sensor(self.appliance2)
        self.url = reverse('collect-by-sha-hmac')

        self.id_int = self.appliance.id
        self.bytes_id = str(self.id_int).encode()

    def test_can_submit_reading(self):
        sensors = {
            self.sensor.code: str(random()),
            self.sensor2.code: str(random()),
            self.sensor3.code: str(random()),
        }
        payload = ["{}={},".format(k, v) for (k, v) in sensors.items()]
        payload += _recent_iso_timestamp()
        payload = "".join(payload)

        binkey = base64.b64decode(self.appliance.authentication_value)
        h = hmac.HMAC(binkey, hashes.SHA256(), backend=default_backend())
        h.update(payload.encode())
        mac = h.finalize()
        b64_mac = base64.b64encode(mac)

        data = {
            'id': self.id_int,
            'data': payload,
            'mac': b64_mac,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 1)
        reading = readings.first()

        sv = SensorValue.objects.filter(sensor=self.sensor, reading=reading)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.value, sensors[self.sensor.code])

        sv = SensorValue.objects.filter(sensor=self.sensor2, reading=reading)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.value, sensors[self.sensor2.code])

        sv = SensorValue.objects.filter(sensor=self.sensor3, reading=reading)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.value, sensors[self.sensor3.code])

    def test_cant_submit_without_correct_mac(self):
        sensors = {
            self.sensor.code: str(random()),
            self.sensor2.code: str(random()),
            self.sensor3.code: str(random()),
        }
        payload = ["{}={},".format(k, v) for (k, v) in sensors.items()]
        payload += _recent_iso_timestamp()
        payload = "".join(payload)

        data = {
            'id': self.id_int,
            'data': payload,
            'mac': "ThisISABadMAC__$%%^",
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_submit_with_bad_timestamp(self):
        sensors = {
            self.sensor.code: str(random()),
            self.sensor2.code: str(random()),
            self.sensor3.code: str(random()),
        }
        payload = ["{}={},".format(k, v) for (k, v) in sensors.items()]
        payload += "BAD_TIMESTAMP"
        payload = "".join(payload)

        binkey = base64.b64decode(self.appliance.authentication_value)
        h = hmac.HMAC(binkey, hashes.SHA256(), backend=default_backend())
        h.update(payload.encode())
        mac = h.finalize()
        b64_mac = base64.b64encode(mac)

        data = {
            'id': self.id_int,
            'data': payload,
            'mac': b64_mac
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_submit_with_empty_payload(self):
        payload = "SomeData"

        binkey = base64.b64decode(self.appliance.authentication_value)
        h = hmac.HMAC(binkey, hashes.SHA256(), backend=default_backend())
        h.update(payload.encode())
        mac = h.finalize()
        b64_mac = base64.b64encode(mac)

        data = {
            'id': self.id_int,
            'data': payload,
            'mac': b64_mac
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_submit_with_bad_payload_format(self):
        payload = "s0:1,s2^12," + _recent_iso_timestamp()

        binkey = base64.b64decode(self.appliance.authentication_value)
        h = hmac.HMAC(binkey, hashes.SHA256(), backend=default_backend())
        h.update(payload.encode())
        mac = h.finalize()
        b64_mac = base64.b64encode(mac)

        data = {
            'id': self.id_int,
            'data': payload,
            'mac': b64_mac
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


def _recent_iso_timestamp():
    date = fake.date_time_this_month().replace(microsecond=0)
    return date.isoformat()
