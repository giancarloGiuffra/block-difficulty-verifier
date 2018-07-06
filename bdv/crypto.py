import hashlib


def double_sha256(content):
    return hashlib.sha256(hashlib.sha256(content).digest()).digest()
