"""
Pydantic schemas for User-related API operations.

Security: UserResponse NEVER includes password hash.
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration request."""
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password must be 8-72 characters"
    )


class UserResponse(BaseModel):
    """Schema for user data in API responses."""
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
