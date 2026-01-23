from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", response_model=TokenResponse)
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    # Prevent user enumeration
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )