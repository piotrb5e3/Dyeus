import os
import base64

from datetime import timezone
from faker import Faker
from appliances.models import Appliance, Reading

fake = Faker()


def create_appliance(owner):
    a = Appliance(
        name=fake.name(),
        authentication_model='token',
        authentication_value=base64.b64encode(os.urandom(32)),
        owner=owner
    )
    a.save()
    return a


def create_sha_authenticated_appliance(owner):
    a = Appliance(
        name=fake.name(),
        authentication_model='sha_hmac',
        authentication_value=base64.b64encode(os.urandom(32)),
        owner=owner
    )
    a.save()
    return a


def create_reading(appliance, timestamp=None):
    if timestamp is None:
        timestamp = fake.date_time_this_month(tzinfo=timezone.utc)
    r = Reading(
        appliance=appliance,
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
    return r
