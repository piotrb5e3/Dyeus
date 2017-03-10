from django.test import TestCase

from appliances.tests.factory import create_appliance
from sensors.tests.factory import create_sensor
from users.tests.factory import create_regular_dyeus_user

from sensors.serializers import SensorSerializer


class TestSensorSerializer(TestCase):
    user = None
    appliance = None
    sensor = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)
        self.sensor = create_sensor(self.appliance)

    def test_serialize(self):
        data = SensorSerializer(self.sensor).data

        self.assertEqual(data['id'], self.sensor.pk)
        self.assertEqual(data['name'], self.sensor.name)
        self.assertEqual(data['code'], self.sensor.code)
        self.assertEqual(data['appliance'], self.appliance.pk)
        self.assertEqual(len(data), 4)

    def test_deserialize(self):
        dirty_data = {
            'id': 42,
            'name': 'Lorem ipsum_23',
            'code': 'some-code-23',
            'appliance': self.appliance.id,
            'sensors': [],
            'owner': 12,
            'extras': {
                'lul': [1, 2, 3],
            }
        }

        serializer = SensorSerializer(data=dirty_data)
        self.assertEqual(serializer.is_valid(), True)

        data = serializer.validated_data

        self.assertRaises(KeyError, lambda: data['id'])
        self.assertEqual(data['name'], dirty_data['name'])
        self.assertEqual(data['code'], dirty_data['code'])
        self.assertEqual(data['appliance'], self.appliance)
        self.assertRaises(KeyError, lambda: data['sensors'])
        self.assertRaises(KeyError, lambda: data['owner'])
        self.assertRaises(KeyError, lambda: data['extras'])

        self.assertEqual(len(data), 3)
