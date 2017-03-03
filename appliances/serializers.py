from rest_framework import serializers
from sensors.serializers import SensorSerializer

from .models import Appliance


class ApplianceSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = Appliance
        fields = ('id', 'name', 'sensors')