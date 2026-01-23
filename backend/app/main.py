from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base

from app.api.users import router as users_router
from app.api.auth import router as auth_router

app = FastAPI(title="Secure Collaborative Platform")

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(users_router)
app.include_router(auth_router)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}