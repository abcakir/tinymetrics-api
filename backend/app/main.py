from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.api.v1 import auth, urls
from app.api import deps
from app.crud.url import get_url_by_short_code

app = FastAPI(title="TinyMetrics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(urls.router, prefix="/api/v1/urls", tags=["URLs"])

@app.get("/")
def read_root():
    return {"status": "active", "service": "TinyMetrics API"}

@app.get("/{short_code}", tags=["redirect"])
def redirect_to_original(short_code: str, db: Session = Depends(deps.get_db)):
    url = get_url_by_short_code(db, short_code)

    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    url.click_count += 1
    db.commit()

    return RedirectResponse(url.original_url)