from random import random
from faker import Faker
from datetime import datetime, timezone

from django.test import TestCase

from appliances.models import Reading
from sensors.models import SensorValue

from appliances.tests.factory import create_appliance
from users.tests.factory import create_regular_dyeus_user
from sensors.tests.factory import create_sensor

from appliances.reading import (_new_reading, new_reading_from_data,
                                ReadingException, )

fake = Faker()


class TestReading(TestCase):
    user = None
    appliance = None
    sensor1 = None
    sensor2 = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)
        self.sensor1 = create_sensor(self.appliance)
        self.sensor2 = create_sensor(self.appliance)

    def test_create_reading(self):
        timestamp = fake.date_time_this_month(tzinfo=timezone.utc)

        r = _new_reading(self.appliance, timestamp=timestamp)
        r.save()

        readings = Reading.objects.filter(appliance=self.appliance,
                                          timestamp=timestamp)
        self.assertEqual(readings.count(), 1)

    def test_create_reading_from_data(self):
        data = {
            self.sensor1.code: str(random()),
            self.sensor2.code: str(random()),
        }

        new_reading_from_data(self.appliance, data,
                              datetime.now(tz=timezone.utc))

        r = Reading.objects.filter(appliance=self.appliance)

        self.assertEqual(r.count(), 1)
        r = r.first()
        self.assertEqual(r.values.count(), 2)

        s = SensorValue.objects.filter(reading=r, sensor=self.sensor1)
        self.assertEqual(s.count(), 1)
        s = s.first()
        self.assertEqual(s.value, data[self.sensor1.code])

        s = SensorValue.objects.filter(reading=r, sensor=self.sensor2)
        self.assertEqual(s.count(), 1)
        s = s.first()
        self.assertEqual(s.value, data[self.sensor2.code])

    def test_create_from_data_raises_on_missing_sensor(self):
        data = {
            self.sensor1.code: str(random()),
        }

        self.assertRaises(ReadingException, new_reading_from_data,
                          self.appliance, data, datetime.now(tz=timezone.utc))

        r = Reading.objects.filter(appliance=self.appliance)

        self.assertEqual(r.count(), 0)
