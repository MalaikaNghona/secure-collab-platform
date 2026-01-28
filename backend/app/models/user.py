"""
User model for database representation.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db.base import Base


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
