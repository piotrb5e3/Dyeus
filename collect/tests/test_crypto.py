import os

from rest_framework.test import APITestCase
from faker import Faker

from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend

from collect.crypto import (CryptoException, sha256_check_mac)

fake = Faker()


class TestCrypto(APITestCase):
    def test_sha256_mac(self):
        plaintext = fake.sentence(nb_words=20).encode()
        key = os.urandom(32)
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(plaintext)
        mac = h.finalize()

        sha256_check_mac(plaintext, key, mac)

    def test_aes256_mac_raises_on_bad_mac(self):
        plaintext = fake.sentence(nb_words=20).encode()
        key = os.urandom(32)
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(plaintext)
        mac = [(b ^ 1) for b in h.finalize()]

        self.assertRaises(CryptoException, sha256_check_mac, plaintext, key,
                          mac)
