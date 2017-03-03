from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import ApplianceViewSet

router = DefaultRouter()
router.register(r'appliances', ApplianceViewSet, base_name='appliance')

urlpatterns = [
    url(r'^', include(router.urls)),
]
