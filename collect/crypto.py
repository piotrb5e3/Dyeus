from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac


def sha256_check_mac(data, key, expected_mac):
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    actual_mac = h.finalize()
    if expected_mac != actual_mac:
        raise CryptoException('Bad MAC')


class CryptoException(Exception):
    pass
