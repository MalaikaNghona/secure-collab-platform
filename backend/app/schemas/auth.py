"""
Pydantic schemas for authentication.
"""
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for login response."""
    access_token: str
    token_type: str
