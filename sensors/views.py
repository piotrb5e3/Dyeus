from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404

from .models import Sensor
from .serializers import SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = get_user(self.request)
        if self.request.user.is_authenticated:
            return Sensor.objects.filter(appliance__owner=user)
        return []

    @detail_route(methods=['get'])
    def recent(self, request, pk=None):
        user = get_user(request)
        sensor = get_object_or_404(Sensor, pk=pk)
        if not sensor.appliance.owner == user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        q = sensor.sensor_values.all().order_by('-reading__timestamp')
        q = q.values_list('value', flat=True)
        values = q[:100]
        return Response({'values': values})
