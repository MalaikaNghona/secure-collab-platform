"""
Security utilities for authentication and authorization.

This module handles:
- Password hashing and verification
- JWT token creation and validation

Security Design Decisions:
1. bcrypt for password hashing (adaptive cost function)
2. Constant-time comparison for password verification
3. JWT with expiration for stateless authentication
4. Secrets loaded from environment configuration
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import get_settings

# Password hashing configuration
# bcrypt is chosen because:
# 1. Adaptive cost function (can be tuned as hardware gets faster)
# 2. Built-in salt generation
# 3. Resistant to rainbow table attacks
# 4. Industry standard for password storage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Security: passlib's verify uses constant-time comparison
    to prevent timing attacks.
    
    Args:
        plain_password: The password to verify
        hashed_password: The bcrypt hash to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Security: bcrypt automatically generates a random salt
    and embeds it in the hash output.
    
    Args:
        password: The plaintext password to hash
        
    Returns:
        The bcrypt hash (includes algorithm, cost, salt, and hash)
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Security Considerations:
    1. Always include expiration (exp claim)
    2. Include issued-at time (iat claim) for auditing
    3. Use UTC timezone to avoid timezone confusion
    4. Don't include sensitive data in payload (it's only signed, not encrypted)
    
    Args:
        data: Claims to include in the token (typically {"sub": user_id})
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT string
    """
    settings = get_settings()
    
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": now,  # Issued at - useful for auditing and token rotation
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.
    
    Security: This function validates:
    1. Signature (token hasn't been tampered with)
    2. Expiration (token hasn't expired)
    3. Algorithm (prevents algorithm confusion attacks)
    
    Args:
        token: The JWT string to decode
        
    Returns:
        The decoded payload if valid, None if invalid
        
    Note:
        Returns None for ANY validation failure to prevent
        information leakage about why validation failed.
    """
    settings = get_settings()
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]  # List prevents algorithm confusion
        )
        return payload
    except JWTError:
        # Don't distinguish between different failure types
        # This prevents attackers from learning about our validation logic
        return None
