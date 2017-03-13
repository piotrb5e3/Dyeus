import os
import binascii
import json

from datetime import datetime, timezone, timedelta
from random import random
from faker import Faker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend

from appliances.tests.factory import (create_appliance,
                                      create_gcm_authenticated_appliance)
from sensors.tests.factory import create_sensor
from users.tests.factory import create_regular_dyeus_user

from appliances.models import Reading

from sensors.models import SensorValue

fake = Faker()


class TestCollectViews(APITestCase):
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
            }
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
            }
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
            }
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 0)

    def test_can_submit_readings(self):
        data = {
            'token': self.appliance.authentication_value,
            'sensors': {
                self.sensor.code: str(random()),
                self.sensor2.code: str(random()),
                self.sensor3.code: str(random()),
            }
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 1)
        reading = readings.first()

        delta = datetime.now(tz=timezone.utc) - reading.timestamp

        self.assertEqual(reading.appliance, self.appliance)
        self.assertLessEqual(delta, timedelta(seconds=5))

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


class TestGCMCollectViews(APITestCase):
    user = None
    appliance = None
    sensor = None
    sensor2 = None
    sensor3 = None
    appliance2 = None
    sensor4 = None
    url = None
    id_int = None
    hex_id = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_gcm_authenticated_appliance(self.user)
        self.appliance.is_active = True
        self.appliance.save()
        self.sensor = create_sensor(self.appliance)
        self.sensor2 = create_sensor(self.appliance)
        self.sensor3 = create_sensor(self.appliance)

        self.appliance2 = create_appliance(self.user)
        self.sensor4 = create_sensor(self.appliance2)
        self.url = reverse('collect-by-gcm-aes')

        self.id_int = self.appliance.id
        self.hex_id = binascii.hexlify(str(self.id_int).encode())

    def test_can_submit_reading(self):
        sensors = {
            self.sensor.code: str(random()),
            self.sensor2.code: str(random()),
            self.sensor3.code: str(random()),
        }
        sensors_bytes = json.dumps(sensors).encode()

        hex_ciphertext, hex_iv, hex_tag = self._enc_helper(sensors_bytes)

        data = {
            'id': self.id_int,
            'iv': hex_iv,
            'sensors': hex_ciphertext,
            'tag': hex_tag,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 1)
        reading = readings.first()

        delta = datetime.now(tz=timezone.utc) - reading.timestamp

        self.assertEqual(reading.appliance, self.appliance)
        self.assertLessEqual(delta, timedelta(seconds=5))

        sv = SensorValue.objects.filter(sensor=self.sensor)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.reading, reading)
        self.assertEqual(sv.value, sensors[self.sensor.code])

        sv = SensorValue.objects.filter(sensor=self.sensor2)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.reading, reading)
        self.assertEqual(sv.value, sensors[self.sensor2.code])

        sv = SensorValue.objects.filter(sensor=self.sensor3)
        self.assertEqual(sv.count(), 1)
        sv = sv.first()
        self.assertEqual(sv.reading, reading)
        self.assertEqual(sv.value, sensors[self.sensor3.code])

    def test_cant_submit_with_malformed_json(self):
        hex_ciphertext, hex_iv, hex_tag = self._enc_helper(b'deadbeefcafebabe')

        data = {
            'id': self.id_int,
            'iv': hex_iv,
            'sensors': hex_ciphertext,
            'tag': hex_tag,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 0)

    def test_cant_submit_without_fields(self):
        sensors = {
            self.sensor.code: str(random()),
            self.sensor2.code: str(random()),
            self.sensor3.code: str(random()),
        }
        sensors_bytes = json.dumps(sensors).encode()

        hex_ciphertext, hex_iv, hex_tag = self._enc_helper(sensors_bytes)

        data = {
            'iv': hex_iv,
            'sensors': hex_ciphertext,
            'tag': hex_tag,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'id': self.id_int,
            'sensors': hex_ciphertext,
            'tag': hex_tag,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'id': self.id_int,
            'iv': hex_iv,
            'tag': hex_tag,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'id': self.id_int,
            'iv': hex_iv,
            'sensors': hex_ciphertext,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        readings = Reading.objects.filter(appliance=self.appliance)
        self.assertEqual(readings.count(), 0)

    def _enc_helper(self, sensors_bytes):
        iv = os.urandom(12)
        hex_iv = binascii.hexlify(iv)
        hex_key = self.appliance.authentication_value
        key = binascii.unhexlify(hex_key)
        enc = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend(),
        ).encryptor()
        associated_data = hex_iv + b'ff' + self.hex_id
        enc.authenticate_additional_data(associated_data)
        ciphertext = enc.update(sensors_bytes) + enc.finalize()
        hex_ciphertext = binascii.hexlify(ciphertext)
        hex_tag = binascii.hexlify(enc.tag)
        return hex_ciphertext, hex_iv, hex_tag
