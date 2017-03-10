from rest_framework.permissions import BasePermission, SAFE_METHODS
from appliances.models import Appliance


class IsInactiveApplianceOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            (request.data and
             request.data['appliance'] and
             Appliance.objects.get(pk=request.data['appliance']) and
             not Appliance.objects.get(pk=request.data['appliance']).is_active
             )
        )
