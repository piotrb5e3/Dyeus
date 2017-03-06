from django.conf.urls import url

from .views import token_collect

urlpatterns = [
    url(r'^collect/token', token_collect),
]
