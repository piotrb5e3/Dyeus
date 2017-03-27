from random import random
from faker import Faker
from sensors.models import Sensor, SensorValue

fake = Faker()


def create_sensor(appliance):
    s = Sensor(
        code=fake.slug(),
        name=fake.name(),
        appliance=appliance
    )
    s.save()
    return s


def create_sensor_value(sensor, reading, value=None):
    if value is None:
        value = random()

    sv = SensorValue(
        sensor=sensor,
        reading=reading,
        value=str(value)
    )
    sv.save()
    return sv
