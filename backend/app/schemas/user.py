from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Basis-Klasse (gemeinsame Felder)
class UserBase(BaseModel):
    email: EmailStr

# Für die Registrierung
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        # Erlaubt Pydantic, Daten direkt aus SQLAlchemy-Models zu lesen
        from_attributes = True