from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from .models import Appliance
from .serializers import ApplianceSerializer


class ApplianceViewSet(viewsets.ModelViewSet):
    serializer_class = ApplianceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Appliance.objects.filter(owner=user)

    def create(self, request):
        data = request.data
        serializer = ApplianceSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)

        appliance = Appliance(
            name=serializer.validated_data['name'],
            authentication_model=(
                serializer.validated_data['authentication_model']),
            owner=request.user)
        appliance.save()

        return Response(ApplianceSerializer(appliance).data,
                        status=status.HTTP_201_CREATED)

    @detail_route(methods=['POST'])
    def activate(self, request, pk=None):
        appliance = get_object_or_404(Appliance, pk=pk, owner=request.user)

        if appliance.is_active:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not appliance.authentication_value:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        appliance.is_active = True
        appliance.save()
        return Response({}, status=status.HTTP_202_ACCEPTED)

    @detail_route(methods=['POST'])
    def deactivate(self, request, pk=None):
        appliance = get_object_or_404(Appliance, pk=pk, owner=request.user)

        if not appliance.is_active:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        appliance.is_active = False
        appliance.save()
        return Response({}, status=status.HTTP_202_ACCEPTED)
