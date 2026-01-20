from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.users import router as users_router

app = FastAPI(title="Secure Collaborative Platform")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include user routes
app.include_router(users_router)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}