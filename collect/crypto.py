import binascii
import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag


def aes128_gcm_encrypt(hex_key, plaintext):
    key = binascii.unhexlify(hex_key)
    assert len(key) == 16

    # Generate a random 96-bit IV.
    iv = os.urandom(12)

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    enc = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend(),
    ).encryptor()

    hex_iv = binascii.hexlify(iv)
    associated_data = hex_iv
    enc.authenticate_additional_data(associated_data)

    ciphertext = enc.update(plaintext) + enc.finalize()

    hex_ciphertext = binascii.hexlify(ciphertext)
    hex_tag = binascii.hexlify(enc.tag)

    return hex_iv, hex_ciphertext, hex_tag


def aes128_gcm_decrypt(hex_key, hex_id, hex_iv, hex_ciphertext, hex_tag):
    key = binascii.unhexlify(hex_key)
    ciphertext = binascii.unhexlify(hex_ciphertext)
    tag = binascii.unhexlify(hex_tag)
    iv = binascii.unhexlify(hex_iv)
    associated_data = hex_iv + b'ff' + hex_id

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    decryptor.authenticate_additional_data(associated_data)

    try:
        return decryptor.update(ciphertext) + decryptor.finalize()
    except InvalidTag:
        raise CryptoException('Bad tag')


class CryptoException(Exception):
    pass