from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404

from .models import Sensor
from .serializers import SensorSerializer
from .permissions import IsInactiveApplianceOrReadOnly


class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsInactiveApplianceOrReadOnly,
                          )

    def get_queryset(self):
        user = self.request.user
        return Sensor.objects.filter(appliance__owner=user)

    @detail_route(methods=['get'])
    def recent(self, request, pk=None):
        user = request.user
        sensor = get_object_or_404(Sensor, pk=pk,
                                   appliance__owner=user)

        q = sensor.sensor_values.all().order_by('-reading__timestamp')
        q = q.values_list('reading__timestamp', 'value')
        values = list(q[:100])
        values.reverse()
        return Response({'values': [[v[0], v[1]] for v in values], })
