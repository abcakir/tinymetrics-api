import string
import random
from sqlalchemy.orm import Session
from app.models.url import Url
from app.schemas.url import UrlCreate

def generate_short_code(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_url(db: Session, url: UrlCreate, user_id: int):
    code = generate_short_code()

    while db.query(Url).filter(Url.short_code == code).first():
        code = generate_short_code()

    db_url = Url(
        original_url=str(url.original_url),
        short_code=code,
        user_id=user_id
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url

def get_urls_by_user(db: Session, user_id: int):
    return db.query(Url).filter(Url.user_id == user_id).all()