import binascii
import json

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from appliances.models import Appliance
from appliances.reading import (new_reading_from_data,
                                ReadingException)

from .crypto import aes128_gcm_decrypt, CryptoException


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


@api_view(['POST'])
def gcm_aes_collect(request):
    if (('id' not in request.data) or
            ('iv' not in request.data) or
            ('sensors' not in request.data) or
            ('tag' not in request.data)):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    int_id = request.data['id']
    encrypted_sensors = request.data['sensors'].encode()
    hex_tag = request.data['tag'].encode()
    hex_iv = request.data['iv'].encode()

    appliances = Appliance.objects.filter(authentication_model='gcm_aes',
                                          pk=int_id)
    if appliances.count() != 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    appliance = appliances.first()

    try:
        hex_key = appliance.authentication_value
        bytes_id = str(int_id).encode()
        decrypted_sensors = aes128_gcm_decrypt(hex_key, bytes_id, hex_iv,
                                               encrypted_sensors,
                                               hex_tag)
        sensors = json.loads(decrypted_sensors)
        new_reading_from_data(appliance, sensors)
        return Response(status=status.HTTP_202_ACCEPTED)

    except CryptoException:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except ReadingException:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except json.decoder.JSONDecodeError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
