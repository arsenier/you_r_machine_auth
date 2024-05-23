import bcrypt


def get_hashed_password(password: str) -> bytes:
    # converting password to array of bytes
    bytes = password.encode("utf-8")
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def check_hashed_password(password: str, hash: bytes) -> bool:
    # encoding user password
    userBytes = password.encode("utf-8")
    # checking password
    result = bcrypt.checkpw(userBytes, hash)
    return result
