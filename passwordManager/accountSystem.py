import hashlib

def hashPassword(password: str):
    """
    Hashes the password in sha256 encoding

    """
    return hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()


if __name__ == '__main__':
    print(hashPassword("password"))

