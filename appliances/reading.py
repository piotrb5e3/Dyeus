from datetime import datetime
from .models import Reading


def new_reading(appliance):
    timestamp = datetime.now()
    return Reading(
        appliance=appliance,
        timestamp=timestamp,
        year=timestamp.year,
        month=timestamp.month,
        day=timestamp.day,
        hour=timestamp.hour,
        minute=timestamp.minute,
        second=timestamp.second,
        microsecond=timestamp.microsecond,
    )
