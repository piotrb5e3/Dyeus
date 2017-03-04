from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
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
            owner=request.user)
        appliance.save()
        return Response(ApplianceSerializer(appliance).data,
                        status=status.HTTP_201_CREATED)
