from datetime import datetime, timezone
from faker import Faker
from django.test import TestCase
from django.core.exceptions import ValidationError

from appliances.models import Appliance, Reading
from appliances.tests.factory import create_appliance
from users.tests.factory import create_regular_dyeus_user

fake = Faker()


class TestApplianceModel(TestCase):
    user = None
    user2 = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.user2 = create_regular_dyeus_user()

    def test_create_appliance(self):
        name = fake.catch_phrase()
        token = fake.password(length=22)
        a = Appliance(
            name=name,
            authentication_model='token',
            authentication_value=token,
            owner=self.user
        )
        a.save()

        appliances = Appliance.objects.filter(name=name, owner=self.user)
        self.assertEqual(appliances.count(), 1)
        a = appliances.first()
        self.assertEqual(a.authentication_model, 'token')
        self.assertEqual(a.authentication_value, token)
        self.assertEqual(a.is_active, False)

    def test_raises_on_repeated_name_with_same_owner(self):
        name = fake.catch_phrase()
        a = Appliance(
            name=name,
            authentication_model='token',
            authentication_value=fake.password(length=22),
            owner=self.user
        )
        a.save()

        a = Appliance(
            name=name,
            authentication_model='token',
            authentication_value=fake.password(length=22),
            owner=self.user
        )
        self.assertRaises(ValidationError, a.save)

    def test_raises_on_repeated_authentication_value(self):
        auth_val = fake.password(length=22)
        a = Appliance(
            name=fake.catch_phrase(),
            authentication_model='token',
            authentication_value=auth_val,
            owner=self.user
        )
        a.save()

        a = Appliance(
            name=fake.catch_phrase(),
            authentication_model='token',
            authentication_value=auth_val,
            owner=self.user2
        )
        self.assertRaises(ValidationError, a.save)


class TestReadingModel(TestCase):
    user = None
    appliance = None

    def setUp(self):
        self.user = create_regular_dyeus_user()
        self.appliance = create_appliance(self.user)

    def test_create_reading(self):
        timestamp = datetime.now(tz=timezone.utc)
        r = Reading(
            appliance=self.appliance,
            year=timestamp.year,
            month=timestamp.month,
            day=timestamp.day,
            hour=timestamp.hour,
            minute=timestamp.minute,
            second=timestamp.second,
            microsecond=timestamp.microsecond,
            timestamp=timestamp
        )
        r.save()

        readings = Reading.objects.filter(timestamp=timestamp)
        self.assertEqual(readings.count(), 1)
        r = readings.first()
        self.assertEqual(r.appliance, self.appliance)
        self.assertEqual(r.timestamp, timestamp)

    def test_raises_on_wrong_year(self):
        timestamp = datetime.now(tz=timezone.utc)
        r = Reading(
            appliance=self.appliance,
            year=timestamp.year + 1,
            month=timestamp.month,
            day=timestamp.day,
            hour=timestamp.hour,
            minute=timestamp.minute,
            second=timestamp.second,
            microsecond=timestamp.microsecond,
            timestamp=timestamp
        )
        self.assertRaises(ValidationError, r.save)

    def test_raises_on_wrong_month(self):
        timestamp = datetime.now(tz=timezone.utc)
        r = Reading(
            appliance=self.appliance,
            year=timestamp.year,
            month=(timestamp.month % 12) + 1,
            day=timestamp.day,
            hour=timestamp.hour,
            minute=timestamp.minute,
            second=timestamp.second,
            microsecond=timestamp.microsecond,
            timestamp=timestamp
        )
        self.assertRaises(ValidationError, r.save)

    def test_raises_on_wrong_hour(self):
        timestamp = datetime.now(tz=timezone.utc)
        r = Reading(
            appliance=self.appliance,
            year=timestamp.year + 1,
            month=timestamp.month,
            day=timestamp.day,
            hour=(timestamp.hour + 1) % 24,
            minute=timestamp.minute,
            second=timestamp.second,
            microsecond=timestamp.microsecond,
            timestamp=timestamp
        )
        self.assertRaises(ValidationError, r.save)

    def test_raises_on_wrong_minute(self):
        timestamp = datetime.now(tz=timezone.utc)
        r = Reading(
            appliance=self.appliance,
            year=timestamp.year + 1,
            month=timestamp.month,
            day=timestamp.day,
            hour=timestamp.hour,
            minute=(timestamp.minute + 1) % 60,
            second=timestamp.second,
            microsecond=timestamp.microsecond,
            timestamp=timestamp
        )
        self.assertRaises(ValidationError, r.save)

    def test_raises_on_wrong_second(self):
        timestamp = datetime.now(tz=timezone.utc)
        r = Reading(
            appliance=self.appliance,
            year=timestamp.year + 1,
            month=timestamp.month,
            day=timestamp.day,
            hour=timestamp.hour,
            minute=timestamp.minute,
            second=(timestamp.second + 1) % 60,
            microsecond=timestamp.microsecond,
            timestamp=timestamp
        )
        self.assertRaises(ValidationError, r.save)

    def test_raises_on_wrong_microsecond(self):
        timestamp = datetime.now(tz=timezone.utc)
        r = Reading(
            appliance=self.appliance,
            year=timestamp.year + 1,
            month=timestamp.month,
            day=timestamp.day,
            hour=timestamp.hour,
            minute=timestamp.minute + 1,
            second=timestamp.second,
            microsecond=(timestamp.microsecond + 1) % 1000,
            timestamp=timestamp
        )
        self.assertRaises(ValidationError, r.save)
