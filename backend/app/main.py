from fastapi import FastAPI

app = FastAPI(title="Secure Collaborative Platform")

@app.get("/health")
def health_check():
    return {"status": "ok"}