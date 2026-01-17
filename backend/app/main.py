from fastapi import FastAPI
<<<<<<< HEAD
from app.db.session import engine
from app.db.base import Base
from app.models import user
from app.api.users import router as users_router

app = FastAPI(title="Secure Collaborative Platform")

Base.metadata.create_all(bind=engine)

app.include_router(users_router)

=======

app = FastAPI(title="Secure Collaborative Platform")

>>>>>>> 3dae59cf8f296ba90c49e5849ffb22ab5b260667
@app.get("/health")
def health_check():
    return {"status": "ok"}