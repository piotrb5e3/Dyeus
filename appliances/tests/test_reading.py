from django.test import TestCase

from appliances.models import Reading
from appliances.tests.factory import create_appliance
from users.tests.factory import create_regular_dyeus_user

from appliances.reading import new_reading


class TestReading(TestCase):
    user = None
    appliance = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)

    def test_create_reading(self):
        r = new_reading(self.appliance)
        timestamp = r.timestamp
        r.save()

        readings = Reading.objects.filter(appliance=self.appliance,
                                          timestamp=timestamp)
        self.assertEqual(readings.count(), 1)
