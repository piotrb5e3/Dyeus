from django.conf.urls import url
from rest_framework.authtoken import views

from .views import auth_test, get_current_user_data

urlpatterns = [
    url(r'^auth/gettoken', views.obtain_auth_token),
    url(r'^auth/test', auth_test),
    url(r'^user', get_current_user_data),
]
