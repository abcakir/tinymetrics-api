from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.core import security
from app.core.security import create_access_token
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user_by_email

router = APIRouter()

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