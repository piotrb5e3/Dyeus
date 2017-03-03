from django.conf.urls import url
from rest_framework.authtoken import views

from .views import auth_test

urlpatterns = [
    url(r'^auth/obtain', views.obtain_auth_token),
    url(r'^auth/test', auth_test),
]
