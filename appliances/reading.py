from django.db import transaction

from appliances.models import Reading
from sensors.models import SensorValue


def new_reading_from_data(appliance, sensors, timestamp):
    appliance_sensors = appliance.sensors.all()

    with transaction.atomic():
        reading = _new_reading(appliance, timestamp)
        reading.save()
        for sensor in appliance_sensors:
            if sensor.code not in sensors:
                raise ReadingException
            value = sensors[sensor.code]
            sv = SensorValue(sensor=sensor,
                             reading=reading,
                             value=str(value))
            sv.save()


def _new_reading(appliance, timestamp):
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


class ReadingException(Exception):
    pass
