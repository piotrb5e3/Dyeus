from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from appliances.models import Appliance
from appliances.reading import new_reading
from sensors.models import SensorValue


@api_view(['POST'])
def token_collect(request):
    token = request.data['token']
    if not token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    appliance = Appliance.objects.filter(authentication_model='token',
                                         authentication_value=token)
    if appliance.count() < 1:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if appliance.count() > 1:
        raise Exception("Assertion error: token matches multiple appliances")

    appliance = appliance.first()
    if not appliance.is_active:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    sensors = request.data['sensors']

    with transaction.atomic():
        reading = new_reading(appliance)
        reading.save()
        for sensor in appliance.sensors.all():
            value = sensors[sensor.code]
            sv = SensorValue(sensor=sensor,
                             reading=reading,
                             value=str(value))
            sv.save()

    return Response(status=status.HTTP_202_ACCEPTED)
