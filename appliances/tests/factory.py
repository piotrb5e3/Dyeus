from faker import Faker
from appliances.models import Appliance

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
