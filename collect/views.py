import binascii
import base64
import dateutil.parser
from datetime import timezone

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from appliances.models import Appliance
from appliances.reading import (new_reading_from_data,
                                ReadingException, )

from .crypto import sha256_check_mac, CryptoException


@api_view(['POST'])
def token_collect(request):
    if any([x not in request.data for x in ['id', 'token', 'sensors']]):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    id = request.data['id']
    token = request.data['token']
    sensors = request.data['sensors']

    appliances = Appliance.objects.filter(id=id, authentication_model='token',
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


@api_view(['POST'])
def sha_hmac_collect(request):
    if any([x not in request.data for x in ['id', 'data', 'mac']]):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    int_id = request.data['id']
    hex_mac = request.data['mac']
    payload = request.data['data']

    appliances = Appliance.objects.filter(authentication_model='sha_hmac',
                                          pk=int_id)
    if appliances.count() != 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    appliance = appliances.first()

    binkey = base64.b64decode(appliance.authentication_value)
    expected_mac = binascii.unhexlify(hex_mac)

    try:
        sha256_check_mac(payload.encode(), binkey, expected_mac)
    except CryptoException:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        sensors = payload.split(',')[:-1]
        dtstr = payload.split(',')[-1]
        sensors = {keqv.split("=")[0]: keqv.split("=")[1] for keqv in sensors}
    except IndexError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        timestamp = dateutil.parser.parse(dtstr).replace(tzinfo=timezone.utc)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        new_reading_from_data(appliance, sensors, timestamp)
        return Response(status=status.HTTP_202_ACCEPTED)
    except ReadingException:
        return Response(status=status.HTTP_400_BAD_REQUEST)
