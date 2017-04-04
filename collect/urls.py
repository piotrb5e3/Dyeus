from django.conf.urls import url

from .views import token_collect, sha_hmac_collect

urlpatterns = [
    url(r'^collect/token/', token_collect, name="collect-by-token"),
    url(r'^collect/sha-hmac/', sha_hmac_collect, name="collect-by-sha-hmac"),
    ]
