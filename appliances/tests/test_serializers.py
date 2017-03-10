from django.test import TestCase

from appliances.tests.factory import create_appliance
from sensors.tests.factory import create_sensor
from users.tests.factory import create_regular_dyeus_user

from appliances.serializers import ApplianceSerializer


class TestApplianceSerializer(TestCase):
    user = None
    appliance = None
    appliance2 = None
    sensor1 = None
    sensor2 = None
    sensor3 = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)
        self.appliance2 = create_appliance(self.user)
        self.sensor1 = create_sensor(self.appliance)
        self.sensor2 = create_sensor(self.appliance)
        self.sensor3 = create_sensor(self.appliance2)

    def test_serialize(self):
        data = ApplianceSerializer(self.appliance).data

        self.assertEqual(data['id'], self.appliance.pk)
        self.assertEqual(data['name'], self.appliance.name)
        self.assertEqual(data['is_active'], self.appliance.is_active)
        self.assertEqual(data['authentication_model'],
                         self.appliance.authentication_model)
        self.assertEqual(data['authentication_value'],
                         self.appliance.authentication_value)
        self.assertEqual(len(data['sensors']), 2)
        self.assertEqual(len(data), 6)

    def test_deserialize(self):
        dirty_data = {
            'id': 42,
            'name': 'Lorem ipsum',
            'is_active': True,
            'authentication_model': 'token',
            'authentication_value': '0xDEADBEEF',
            'sensors': [],
            'owner': 12,
            'extras': {
                'lul': [1, 2, 3],
            }
        }

        serializer = ApplianceSerializer(data=dirty_data)

        self.assertEqual(serializer.is_valid(), True)
        data = serializer.validated_data

        self.assertRaises(KeyError, lambda: data['id'])
        self.assertEqual(data['name'], dirty_data['name'])
        self.assertRaises(KeyError, lambda: data['is_active'])
        self.assertEqual(data['authentication_model'],
                         data['authentication_model'])
        self.assertRaises(KeyError, lambda: data['authentication_value'])
        self.assertRaises(KeyError, lambda: data['sensors'])
        self.assertRaises(KeyError, lambda: data['owner'])
        self.assertRaises(KeyError, lambda: data['extras'])
        self.assertEqual(len(data), 2)
