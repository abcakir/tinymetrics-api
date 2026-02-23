from fastapi import FastAPI
from app.api.v1 import auth

app = FastAPI(title="TinyMetrics API")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"status": "active", "service": "TinyMetrics API"}