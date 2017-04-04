from django.conf.urls import url

from .views import token_collect, gcm_aes_collect, sha_hmac_collect

urlpatterns = [
    url(r'^collect/token/', token_collect, name="collect-by-token"),
    url(r'^collect/gcm-aes/', gcm_aes_collect, name="collect-by-gcm-aes"),
    url(r'^collect/sha-hmac/', sha_hmac_collect, name="collect-by-sha-hmac"),
]
