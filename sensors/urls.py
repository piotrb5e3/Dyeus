from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet

router = DefaultRouter()
router.register(r'sensors', SensorViewSet, base_name='sensor')

urlpatterns = [
    url(r'^', include(router.urls)),
]
