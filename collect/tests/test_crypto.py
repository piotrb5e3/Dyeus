import binascii
import os

from rest_framework.test import APITestCase
from random import randint
from faker import Faker

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend

from collect.crypto import (aes128_gcm_encrypt, aes128_gcm_decrypt,
                            CryptoException, sha256_check_mac)

fake = Faker()


class TestCrypto(APITestCase):
    def test_can_encrypt(self):
        plaintext = fake.sentence(nb_words=20).encode()
        key = os.urandom(16)

        hex_key = binascii.hexlify(key)
        hex_iv, hex_ciphertext, hex_tag = aes128_gcm_encrypt(hex_key,
                                                             plaintext)

        iv = binascii.unhexlify(hex_iv)
        tag = binascii.unhexlify(hex_tag)
        ciphertext = binascii.unhexlify(hex_ciphertext)

        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()

        decryptor.authenticate_additional_data(hex_iv)

        decrypted_plaintext = (
            decryptor.update(ciphertext) + decryptor.finalize())

        self.assertEqual(plaintext, decrypted_plaintext)

    def test_can_decrypt(self):
        hex_ctxt, hex_id, hex_iv, hex_key, hex_tag, plaintext = _helper_enc()

        decrypted_plaintext = aes128_gcm_decrypt(hex_key, hex_id, hex_iv,
                                                 hex_ctxt, hex_tag)

        self.assertEqual(plaintext, decrypted_plaintext)

    def test_raises_on_bad_tag(self):
        hex_ctxt, hex_id, hex_iv, hex_key, hex_tag, plaintext = _helper_enc()
        bad_tag = _hex_mangle(hex_tag)

        self.assertRaises(CryptoException, aes128_gcm_decrypt, hex_key, hex_id,
                          hex_iv, hex_ctxt, bad_tag)

    def test_raises_on_bad_ciphertext(self):
        hex_ctxt, hex_id, hex_iv, hex_key, hex_tag, plaintext = _helper_enc()
        bad_ciphtxt = _hex_mangle(hex_tag)

        self.assertRaises(CryptoException, aes128_gcm_decrypt, hex_key, hex_id,
                          hex_iv, bad_ciphtxt, hex_tag)

    def test_raises_on_bad_iv(self):
        hex_ctxt, hex_id, hex_iv, hex_key, hex_tag, plaintext = _helper_enc()
        bad_iv = _hex_mangle(hex_iv)

        self.assertRaises(CryptoException, aes128_gcm_decrypt, hex_key, hex_id,
                          bad_iv, hex_ctxt, hex_tag)

    def test_raises_on_bad_id(self):
        hex_ctxt, hex_id, hex_iv, hex_key, hex_tag, plaintext = _helper_enc()
        bad_id = _hex_mangle(hex_id)

        self.assertRaises(CryptoException, aes128_gcm_decrypt, hex_key, bad_id,
                          hex_iv, hex_ctxt, hex_tag)

    def test_raises_on_bad_key(self):
        hex_ctxt, hex_id, hex_iv, hex_key, hex_tag, plaintext = _helper_enc()
        bad_key = _hex_mangle(hex_key)

        self.assertRaises(CryptoException, aes128_gcm_decrypt, bad_key, hex_id,
                          hex_iv, hex_ctxt, hex_tag)

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


def _helper_enc():
    """
    Prepare data for testing decryption
    """
    plaintext = fake.sentence(nb_words=20).encode()
    key = os.urandom(16)
    iv = os.urandom(12)
    id = str(randint(1, 2 ** 31)).encode()
    hex_key = binascii.hexlify(key)
    hex_iv = binascii.hexlify(iv)
    bytes_id = str(id).encode()
    enc = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend(),
    ).encryptor()
    enc.authenticate_additional_data(hex_iv + b'ff' + bytes_id)
    ciphertext = enc.update(plaintext) + enc.finalize()
    hex_ciphertext = binascii.hexlify(ciphertext)
    hex_tag = binascii.hexlify(enc.tag)
    return hex_ciphertext, bytes_id, hex_iv, hex_key, hex_tag, plaintext


def _hex_mangle(to_mangle):
    """Returns a hex bytes string that is different than input
    (but of same length)"""
    return bytes(ord('f' if e != ord('f') else '0') for e in to_mangle)
