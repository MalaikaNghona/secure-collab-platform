from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, RegisterResponse, UserResponse
from app.core.security import get_password_hash
from app.core.jwt import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=RegisterResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires
    )

    return {
        "user": UserResponse(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name
        ),
        "access_token": access_token,
        "token_type": "bearer"
    }