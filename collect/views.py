from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from appliances.models import Appliance
from appliances.reading import new_reading
from sensors.models import SensorValue


@api_view(['POST'])
def token_collect(request):
    if ('token' not in request.data) or ('sensors' not in request.data):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    token = request.data['token']

    appliances = Appliance.objects.filter(authentication_model='token',
                                          authentication_value=token)
    if appliances.count() != 1:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    appliance = appliances.first()
    if not appliance.is_active:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    sensors = request.data['sensors']

    appliance_sensors = appliance.sensors.all()

    if len(sensors) != appliance.sensors.count():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    for sensor in appliance_sensors:
        if sensor.code not in sensors:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        reading = new_reading(appliance)
        reading.save()
        for sensor in appliance_sensors:
            value = sensors[sensor.code]
            sv = SensorValue(sensor=sensor,
                             reading=reading,
                             value=str(value))
            sv.save()

    return Response(status=status.HTTP_202_ACCEPTED)
