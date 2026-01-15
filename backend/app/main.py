from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.models import user  # important: imports the model

app = FastAPI(title="Secure Collaborative Platform")

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}