from rest_framework.permissions import BasePermission, SAFE_METHODS
from sensors.models import Sensor
from appliances.models import Appliance


class IsInactiveApplianceOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'DELETE' and 'pk' in view.kwargs:
            pk = view.kwargs['pk']
            s = Sensor.objects.filter(pk=pk)
            return s.count() == 1 and not s.first().appliance.is_active

        if (request.method == 'PUT'
                and 'appliance' in request.data
                and 'pk' in view.kwargs):
            a_old = Appliance.objects.filter(pk=view.kwargs['pk'],
                                             owner=request.user)
            a_new = Appliance.objects.filter(pk=request.data['appliance'],
                                             owner=request.user)
            if a_old.count() == 1 and a_new.count() == 1:
                a_old = a_old.first()
                a_new = a_new.first()
                return (not a_old.is_active) and (not a_new.is_active)

        if request.method == 'POST' and 'appliance' in request.data:
            a = Appliance.objects.filter(pk=request.data['appliance'],
                                         owner=request.user)
            if a.count() == 1:
                a = a.first()
                return not a.is_active

        return False
