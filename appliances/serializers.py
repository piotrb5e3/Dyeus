from rest_framework import serializers
from sensors.serializers import SensorSerializer

from .models import Appliance


class ApplianceSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = Appliance
        fields = ('id', 'name', 'sensors', 'is_active', 'authentication_model',
                  'authentication_value')
        read_only_fields = ('sensors', 'is_active')
        extra_kwargs = {'authentication_value': {'write_only': True}}
