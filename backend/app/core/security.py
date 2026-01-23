from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

MAX_BCRYPT_PASSWORD_BYTES = 75

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > MAX_BCRYPT_PASSWORD_BYTES:
        password_bytes = password_bytes[:MAX_BCRYPT_PASSWORD_BYTES]

    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")

    if len(password_bytes) > MAX_BCRYPT_PASSWORD_BYTES:
        password_bytes = password_bytes[:MAX_BCRYPT_PASSWORD_BYTES]

    return pwd_context.verify(password_bytes, hashed_password)