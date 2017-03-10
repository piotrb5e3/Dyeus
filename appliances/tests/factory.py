from datetime import datetime, timezone
from faker import Faker
from appliances.models import Appliance, Reading

fake = Faker()


def create_appliance(owner):
    a = Appliance(
        name=fake.name(),
        authentication_model='token',
        authentication_value=fake.password(length=22),
        owner=owner
    )
    a.save()
    return a


def create_reading(appliance):
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
