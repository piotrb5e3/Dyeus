from random import random
from faker import Faker
from django.test import TestCase
from django.core.exceptions import ValidationError

from sensors.models import Sensor, SensorValue

from appliances.tests.factory import create_appliance, create_reading
from users.tests.factory import create_regular_dyeus_user
from sensors.tests.factory import create_sensor

fake = Faker()


class TestSensorModel(TestCase):
    user = None
    appliance = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)

    def test_create_sensor(self):
        code = fake.slug()
        name = fake.name()
        s = Sensor(code=code,
                   name=name,
                   appliance=self.appliance)
        s.save()

        sensors = Sensor.objects.filter(appliance=self.appliance,
                                        code=code)
        self.assertEqual(sensors.count(), 1)

        s = sensors.first()
        self.assertEqual(s.name, name)

    def test_raises_on_repeated_code_with_same_appliance(self):
        code = fake.slug()
        s = Sensor(code=code,
                   name=fake.name(),
                   appliance=self.appliance)
        s.save()

        s = Sensor(code=code,
                   name=fake.name(),
                   appliance=self.appliance)
        self.assertRaises(ValidationError, s.save)

    def test_raises_on_repeated_name_with_same_appliance(self):
        name = fake.name()
        s = Sensor(code=fake.slug(),
                   name=name,
                   appliance=self.appliance)
        s.save()

        s = Sensor(code=fake.slug(),
                   name=name,
                   appliance=self.appliance)
        self.assertRaises(ValidationError, s.save)


class TestSensorValueModel(TestCase):
    user = None
    appliance = None
    sensor = None
    reading = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)
        self.sensor = create_sensor(self.appliance)
        self.reading = create_reading(self.appliance)

    def test_can_create_sensor_value(self):
        sv = SensorValue(sensor=self.sensor,
                         reading=self.reading,
                         value=str(random()))
        sv.save()

    def test_raises_on_duplicate_reading_for_sensor_in_reading(self):
        sv = SensorValue(sensor=self.sensor,
                         reading=self.reading,
                         value=str(random()))
        sv.save()
        sv = SensorValue(sensor=self.sensor,
                         reading=self.reading,
                         value=str(random()))
        self.assertRaises(ValidationError, sv.save)

    def test_raises_on_empty_string_value(self):
        sv = SensorValue(sensor=self.sensor,
                         reading=self.reading,
                         value="")
        self.assertRaises(ValidationError, sv.save)
