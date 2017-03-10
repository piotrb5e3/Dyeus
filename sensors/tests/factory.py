from faker import Faker
from sensors.models import Sensor

fake = Faker()


def create_sensor(appliance):
    s = Sensor(
        code=fake.slug(),
        name=fake.name(),
        appliance=appliance
    )
    s.save()
    return s
