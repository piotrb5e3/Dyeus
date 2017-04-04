import os
import base64

from datetime import datetime, timezone
from faker import Faker
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

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
        token = base64.b64encode(os.urandom(32)).decode()
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

    def test_create_appliance_no_auth_value(self):
        name = fake.catch_phrase()
        a = Appliance(
            name=name,
            authentication_model='token',
            owner=self.user
            )
        a.save()

        appliances = Appliance.objects.filter(name=name, owner=self.user)
        self.assertEqual(appliances.count(), 1)
        a = appliances.first()
        self.assertEqual(a.authentication_model, 'token')
        self.assertEqual(a.is_active, False)

    def test_raises_on_repeated_name_with_same_owner(self):
        name = fake.catch_phrase()
        a = Appliance(
            name=name,
            authentication_model='token',
            authentication_value=base64.b64encode(os.urandom(32)),
            owner=self.user
            )
        a.save()

        a = Appliance(
            name=name,
            authentication_model='token',
            authentication_value=base64.b64encode(os.urandom(32)),
            owner=self.user
            )
        self.assertRaises(ValidationError, a.save)

    def test_raises_on_too_weak_authentication_value(self):
        name = fake.catch_phrase()
        a = Appliance(
            name=name,
            authentication_model='token',
            authentication_value=base64.b64encode(os.urandom(10)),
            owner=self.user
            )
        self.assertRaises(ValidationError, a.save)

    def test_raises_on_null_authentication_value(self):
        name = fake.catch_phrase()
        a = Appliance(
            name=name,
            authentication_model='token',
            authentication_value=None,
            owner=self.user
            )
        self.assertRaises(IntegrityError, a.save)


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
