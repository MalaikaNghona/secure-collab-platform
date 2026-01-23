from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

MAX_PASSWORD_BYTES = 72

def _truncate(password: str) -> bytes:
    pw_bytes = password.encode("utf-8")
    return pw_bytes[:MAX_PASSWORD_BYTES]

def hash_password(password: str) -> str:
    return pwd_context.hash(_truncate(password))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_truncate(plain_password), hashed_password)