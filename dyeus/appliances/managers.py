from dyeus.db import DBSession
from dyeus.models import Appliance


def get_all_appliances():
    return DBSession.query(Appliance).all()
