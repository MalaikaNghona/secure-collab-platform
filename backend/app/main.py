from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.models import user
from app.api.users import router as users_router

app = FastAPI(title="Secure Collaborative Platform")

Base.metadata.create_all(bind=engine)

app.include_router(users_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}