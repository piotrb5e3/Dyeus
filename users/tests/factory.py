from users.models import DyeusUser
from faker import Faker

fake = Faker()


def create_regular_dyeus_user():
    user = DyeusUser(username=fake.user_name(),
                     email=fake.email(),
                     password=fake.password())
    user.save()
    return user
