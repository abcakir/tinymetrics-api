import httpx
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.api import deps
from app import crud
from fastapi.responses import RedirectResponse
from app.core import security
from app.core.security import create_access_token
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user_by_email
from app.core.config import settings

router = APIRouter()

GITHUB_CLIENT_ID = settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Prüfen: Gibt es die Email schon?
    existing_user = get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 2. Erstellen: CRUD aufrufen
    new_user = create_user(db=db, user=user_in)

    return new_user

@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.user.get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="E-Mail oder Passwort falsch.")
    if not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="E-Mail oder Passwort falsch.")
    access_token = create_access_token(subject=user.id)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/github/login")
def github_login():
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=user:email")

@router.get("/github/callback")
async def github_callback(code: str, db: Session = Depends(deps.get_db)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
        )
        token_json = token_response.json()
        access_token = token_json.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get token from GitHub")
        
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_response.json()

        email = user_data.get("email")
        if not email:
            email_response = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            email_data = email_response.json()

            for e in email_data:
                if e.get("primary") and e["verified"]:
                    email = e["email"]
                    break
            
            if not email:
                raise HTTPException(status_code=400, detail="No verified email found on GitHub")
            
        user = get_user_by_email(db, email=email)

        if not user:
            import secrets
            random_password = secrets.token_urlsafe(16)

            user_in = UserCreate(email=email, password=random_password)
            user = create_user(db=db, user=user_in)
        
        access_token = create_access_token(subject=user.id)
        return {"access_token": access_token, "token_type": "bearer", "message": "Login successful"}