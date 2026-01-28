"""
Authentication endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and receive JWT access token.
    
    Security:
    - Same error for invalid email AND password (prevents enumeration)
    - Uses OAuth2 form for Swagger UI compatibility
    """
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if user is None:
        raise invalid_credentials
    
    if not verify_password(form_data.password, user.hashed_password):
        raise invalid_credentials
    
    if not user.is_active:
        raise invalid_credentials
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return Token(access_token=access_token, token_type="bearer")
