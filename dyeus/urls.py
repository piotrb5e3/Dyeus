from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from appliances.urls import urlpatterns as appliances_urls
from sensors.urls import urlpatterns as sensors_urls
from users.urls import urlpatterns as users_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(appliances_urls)),
    url(r'^', include(sensors_urls)),
    url(r'^', include(users_urls))
]

if settings.DEBUG:
    urlpatterns.append(
        url(r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework')))
