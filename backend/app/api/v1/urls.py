from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.url import UrlCreate, UrlResponse
from app.models.user import User
from app.crud.url import create_url, get_urls_by_user
from app.api import deps

router = APIRouter()

@router.post("/", response_model=UrlResponse, status_code=201)
def create_new_url(url_in: UrlCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)) -> Any:
    """Create new URL, only for authenticated users"""
    return create_url(db=db, url=url_in, user_id=current_user.id)

@router.get("/me", response_model=List[UrlResponse])
def read_user_urls(db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)) -> Any:
    """Get all URLs for the authenticated user"""
    return get_urls_by_user(db=db, user_id=current_user.id)