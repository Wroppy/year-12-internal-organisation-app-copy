import hashlib

def hashPassword(password: str):
    return hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()

