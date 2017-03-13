from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from appliances.models import Appliance
from appliances.reading import (new_reading_from_data,
                                ReadingException)


@api_view(['POST'])
def token_collect(request):
    if ('token' not in request.data) or ('sensors' not in request.data):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    token = request.data['token']
    sensors = request.data['sensors']

    appliances = Appliance.objects.filter(authentication_model='token',
                                          authentication_value=token,
                                          is_active=True)
    if appliances.count() != 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    appliance = appliances.first()

    try:
        new_reading_from_data(appliance, sensors)
    except ReadingException:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_202_ACCEPTED)
